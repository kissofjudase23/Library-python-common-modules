# -*- coding: utf-8 -*-


# Module Base Error
class ModuleError(ValueError):
    pass


class ArgError(ModuleError):
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


# File Error
class FileError(ModuleError):
    pass


class HDFSError(FileError):
    pass
