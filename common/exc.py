#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BaseError(ValueError):
    pass


class AwsBaseError(BaseError):
    pass


class SQSBaseError(AwsBaseError):
    pass


class SendMsgError(SQSBaseError):
    pass


class DelMsgError(SQSBaseError):
    pass


class ReceiveMsgError(SQSBaseError):
    pass


class NoMatchQueueError(SQSBaseError):
    pass


class FileBaseError(BaseError):
    pass

class HDFSError(FileBaseError):
    pass

