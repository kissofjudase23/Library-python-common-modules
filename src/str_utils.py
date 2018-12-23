#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class StrUtils(object):

    @classmethod
    def to_str(cls, bytes_or_str):
        """

        :param bytes_or_str:
        :return: unicode string
        """
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str

        return value

    @classmethod
    def to_bytes(cls, bytes_or_str):
        """

        :param bytes_or_str:
        :return: bytes string
        """
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode('utf-8')
        else:
            value = bytes_or_str

        return value
