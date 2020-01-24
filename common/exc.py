# -*- coding: utf-8 -*-


# Module Base Error
class ModuleError(ValueError):
    pass


class ArgError(ModuleError):
    pass


class SubProcessError(ModuleError):
    pass


# AWS Error
class AwsError(ModuleError):
    pass


# SQS Error
class SQSError(AwsError):
    pass


class SendMsgError(SQSError):
    pass


class DelMsgError(SQSError):
    pass


class ReceiveMsgError(SQSError):
    pass


class NoMatchQueueError(SQSError):
    pass


# SSM Error
class SSMError(AwsError):
    pass


class SSMListParameterError(SSMError):
    pass


class S3Error(AwsError):
    pass


class GetVersionIDError(S3Error):
    pass


class CopyObjectError(S3Error):
    pass


class PutObjectError(S3Error):
    pass


class UploadFileError(S3Error):
    pass


class DownloadFileError(S3Error):
    pass


class ListObjectError(S3Error):
    pass


class DeleteObjectError(S3Error):
    pass


# File Error
class FileError(ModuleError):
    pass


class HDFSError(FileError):
    pass


class ParseError(ModuleError):
    pass


class TokenizeError(ModuleError):
    pass
