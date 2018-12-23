#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from ..str_utils import StrUtils


class TestEncodeFormatter(object):

    @pytest.mark.parametrize('str_, assert_str', [
        pytest.param('utf8_str', 'utf8_str'),
        pytest.param(b'bytes_str', 'bytes_str')
    ])
    def test_to_utf8_str(self, str_, assert_str):

        utf8_str = StrUtils.to_str(str_)

        assert isinstance(utf8_str, str)
        assert utf8_str == assert_str

    @pytest.mark.parametrize('str_, assert_str', [
        pytest.param('utf8_str', b'utf8_str'),
        pytest.param(b'bytes_str', b'bytes_str')
    ])
    def test_to_bytes_str(self, str_, assert_str):
        bytes_str = StrUtils.to_bytes(str_)

        assert isinstance(bytes_str, bytes)
        assert bytes_str == assert_str


