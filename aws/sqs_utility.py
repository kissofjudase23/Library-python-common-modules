#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config



class NoMatchQueueError(ValueError):
    pass


class SendMessageError(ValueError):
    pass


class SQSUtility(object):
    """
    Please refer
    http://boto3.readthedocs.io/en/latest/reference/services/sqs.html
    for detail
    """

    instance = None

    @classmethod
    def get_instance(cls, logger, max_retry=3):
        if not cls.instance:
            cls.instance = SQSUtility(logger, max_retry)

        return cls.instance

    def __init__(self, logger, max_retry=3):

        retry_config = Config(
            retries=dict(
                max_attempts=max_retry
            )
        )

        self.sqs = boto3.client(service_name='sqs',
                                config=retry_config)
        self.logger = logger

    def list_queue_url(self, queue_name_prefix):
        """ get queue url from prefix of queue name

        param:
            queue_name_prefix: prefix of queue name
        return:
            list of queue_url
        Raise:
            NoMatchQueueError
        """
        try:
            res = self.sqs.list_queues(QueueNamePrefix=queue_name_prefix)

            if 'QueueUrls' in res:
                return res['QueueUrls']
            else:
                self.logger.info("No match url with the name prefix{0}"
                                 .format(queue_name_prefix))
                raise NoMatchQueueError()

        except ClientError as e:
            self.logger.error(e)
            raise e

    def delete_message(self, queue_url, receipt_handle):
        """
        param:
            queue_url: url of queue
            receipt_handle: The receipt handle associated with the message
                            to delete.
        return:
            None
        """
        try:
            self.sqs.delete_message(QueueUrl=queue_url,
                                    ReceiptHandle=receipt_handle)
        except ClientError as e:
            self.logger.error(e)
            raise e

    def receive_message(self,
                        queue_url,
                        max_num_msg=1, wait_time_secs=0):
        """
        param:
            queue_url: url of queue
            max_num_msg: batch mode, maximum of this number is 10
            wait_time_secs: The duration (in seconds) for which the call waits
                            for a message to arrive in the queue before returning.
        return:
            None: No message
            List of message dict
        """
        try:
            attribute_name = ['all']

            res = self.sqs.receive_message(QueueUrl=queue_url,
                                           WaitTimeSeconds=wait_time_secs,
                                           AttributeNames=attribute_name,
                                           MaxNumberOfMessages=max_num_msg)

            if 'Messages' not in res:
                return None

            return res['Messages']

        except ClientError as e:
            self.logger.error(e)
            raise e

    def send_message(self,
                     queue_url,
                     msg_body,
                     msg_type,
                     msg_deduplication_id,
                     msg_group_id):
        """
        param
            queue_url: url of queue
            msg_body:  body of msg
            msg_type:  type of msg, please refer MSG_TYPE
            msg_deduplication_id: dedupliation id of the msg
            msg_group_id: group id of the msg
        return:
            None
        Raise:
            SendMessageError
        """
        try:
            res = self.sqs.send_message(QueueUrl=queue_url,
                                        MessageBody=msg_body,
                                        MessageDeduplicationId=msg_deduplication_id,
                                        MessageGroupId=msg_group_id,
                                        MessageAttributes={
                                            'msg_type': {
                                                          'DataType': 'Number',
                                                          'StringValue': str(msg_type)
                                            }})

            # An MD5 digest of the non-URL-encoded message attribute string.
            if 'MD5OfMessageBody' not in res:
                self.logger.warn("Does not receive MD5OfMessageBody, msg_body="
                                 .format(msg_body))
                raise SendMessageError("Does not receive MD5OfMessageBody")

            res_md5_of_msg_body = res['MD5OfMessageBody']
            if res_md5_of_msg_body != hashlib.md5(msg_body.encode()).hexdigest():
                self.logger.warn("response md5 is not as expected, msg_body={}"
                                 .format(msg_body))
                raise SendMessageError("MD5OfMessageBody Check Failed")

        except ClientError as e:
            self.logger.error(e)
            raise e


if __name__ == '__main__':
    pass
