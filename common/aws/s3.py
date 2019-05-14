# -*- coding: utf-8 -*-

import os
import sys

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from ..exc import GetVersionIDError, CopyObjectError, PutObjectError, UploadFileError,\
                DownloadFileError, DownloadFileError, ListObjectError, DeleteObjectError


class S3Wrapper(object):

    def __init__(self, *, max_retry=3):
        retry_config = Config(
            retries=dict(
                max_attempts=max_retry
            )
        )

        self.s3 = boto3.client(service_name="s3",
                               config=retry_config)

    def get_latest_version_id_from_key(self, bucket, key, *, max_keys=1):
        kwargs = {'Bucket': bucket,
                  'Prefix': key,
                  'MaxKeys': max_keys}
        try:
            while True:
                res = self.s3.list_object_versions(**kwargs)

                if 'Versions' not in res:
                    return None

                for d in res['Versions']:
                    if d['IsLatest']:
                        return d['VersionId']

                if not res['IsTruncated']:
                    break

                kwargs['KeyMarker'] = res['NextKeyMarker']

            return None
        except ClientError as e:
            raise GetVersionIDError(f'get latest verion id of {bucket}/{key}'
                                    f' failed, err:{e}') from e

    def copy_object(self,
                    src_bucket,
                    src_key,
                    dest_bucket,
                    dest_key,
                    version_id=None,
                    sse_alg='AES256',
                    metadata_directive='COPY'):
        """ The object is transfered from s3 to s3 (do not land in the local)
        """
        copy_source = {'Bucket': src_bucket,
                       'Key': src_key}

        if version_id:
            copy_source['VersionId'] = version_id

        try:
            self.s3.copy_object(ACL='bucket-owner-full-control',
                                CopySource=copy_source,
                                Bucket=dest_bucket,
                                Key=dest_key,
                                ServerSideEncryption=sse_alg,
                                MetadataDirective=metadata_directive)

        except ClientError as e:
            raise CopyObjectError(f'copy object from {src_bucket}/{src_key}'
                                  f'to {dest_bucket}/{dest_key} failed, err:{e}') from e

    def put_object(self, src_obj, bucket_name, key, *, sse_alg='AES256'):

        kwargs = {'Bucket': bucket_name,
                  'Key': key,
                  'Body': src_obj,
                  'ServerSideEncryption': sse_alg}
        try:
            self.s3.put_object(**kwargs)

        except ClientError as e:
            raise PutObjectError(f'put object to {bucket_name}/{key} failed, err:{e}') from e

    def upload_file(self, bucket, key, file_path):
        try:
            self.s3.upload_file(file_path, bucket, key)
        except ClientError as e:
            raise UploadFileError(f'upload {file_path} to {bucket}/{key} failed'
                                  f'err:{e}') from e

    def download_file(self, bucket, key, file_path):
        try:
            self.s3.download_file(bucket, key, file_path)
        except ClientError as e:
            raise DownloadFileError(f'downlod {bucket}/{key} to {file_path} to failed'
                                    f'err:{e}') from e

    def list_objects_iter(self,
                          bucket,
                          *,
                          prefix=None,
                          delimiter=None,
                          start_after=None):

        """
        StartAfter: (improve performance)
        is where you want Amazon S3 to start listing from.
        Amazon S3 starts listing after this specified key.
        StartAfter can be any key in the bucket
        """

        kwargs = {'Bucket': bucket}
        if prefix:
            kwargs['Prefix'] = prefix

        if delimiter:
            kwargs['Delimiter'] = delimiter

        if start_after:
            kwargs['StartAfter'] = start_after

        while True:
            try:
                res = self.s3.list_objects_v2(**kwargs)
            except ClientError as e:
                raise ListObjectError(f'list objects failed, bucket:{bucket},'
                                      f'prefix:{prefix}, start_after:{start_after}, err:{e}') from e

            # nothing returned
            if 'Contents' not in res:
                break

            for obj in res['Contents']:
                yield obj

            if not res['IsTruncated']:
                break

            kwargs['ContinuationToken'] = res['NextContinuationToken']

    def list_objects(self,
                     bucket,
                     *,
                     prefix=None,
                     delimiter=None,
                     start_after=None,
                     sort_key='LastModified',
                     reverse=True,
                     limit=550):

        """ list all s3 objects, sort by key and return limit number
        """
        kwargs = {'Bucket': bucket}

        if prefix:
            kwargs['Prefix'] = prefix

        if delimiter:
            kwargs['Delimiter'] = delimiter

        if start_after:
            kwargs['StartAfter'] = start_after

        objs = list()
        while True:
            try:
                # Returns some or all (up to 1000) of the objects in a bucket.
                res = self.s3.list_objects_v2(**kwargs)
            except ClientError as e:
                raise ListObjectError(f'list objects failed, bucket:{bucket},'
                                      f'prefix:{prefix}, start_after:{start_after}, err:{e}') from e

            # nothing returned
            if 'Contents' not in res:
                break

            objs.extend(res['Contents'])

            # if there is no sorting requirements, just break when over limit
            # sorting need to iterate all
            if not sort_key:
                if limit and len(objs) >= limit:
                    break

            if not res['IsTruncated']:
                break

            # NextContinuationToken is sent when isTruncated is true which means
            # there are more keys in the bucket that can be listed.
            kwargs['ContinuationToken'] = res['NextContinuationToken']

        if sort_key:
            objs = sorted(objs, key=lambda x: x[sort_key], reverse=reverse)

        if limit:
            return objs[:limit]

        return objs

    def delete_all(self, bucket, *, prefix=None, delimiter=None, start_after=None):
        # This operation enables you to delete multiple objects from a bucket
        # using a single HTTP request. You may specify up to 1000 keys.

        batch_objs_list = list()
        batch_objs = list()

        count = 0
        objs = self.list_objects_iter(bucket,
                                      prefix=prefix,
                                      delimiter=delimiter,
                                      start_after=start_after)

        for obj in objs:
            batch_objs.append({'Key': obj['Key']})
            count += 1
            # One batch puts 1000 objects
            if count % 1000 == 0:
                batch_objs_list.append(batch_objs)
                # create a new list for next batch, do not use clear() here.
                batch_objs = list()

        # last batch
        batch_objs_list.append(batch_objs)

        for batch_objs in batch_objs_list:

            if not batch_objs:
                continue

            try:
                self.s3.delete_objects(
                    Bucket=bucket,
                    Delete={
                        'Objects': batch_objs
                    }
                )
            except ClientError as e:
                raise DeleteObjectError(f'delete objects failed, bucket:{bucket}, '
                                        f'prefix:{prefix}, start_after:{start_after},'
                                        f'err:{e}') from e

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
