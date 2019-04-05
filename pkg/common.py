import re


class Utils(object):

    @staticmethod
    def is_equal(data, test_case):
        if data == test_case:
            return True
        return False

    @staticmethod
    def is_re_match(data, test_case):
        if re.match(data, test_case, re.IGNORECASE):
            return True
        return False

    @staticmethod
    def compile_regex_data(data_list):
        """ Compile regex object from the data_list
            It's ok even the data_list is empty

        :param data_list:
        :return:
            compiled regex object
            empty list
        """

        # TODO, fix here
        # It is tricky here, since compiled regex from empty list would match anything
        # However, return empty list is not a good idea too
        # try to raise some useful info to let caller decide what to do
        if not data_list:
            return list()

        # re format should be  (expression1|expression2|expression3
        data_list_re = f"({'|'.join(data_list)})"

        compiled_data_list_re = re.compile(data_list_re, re.IGNORECASE)

        return compiled_data_list_re

    @staticmethod
    def compile_exactly_regex_data(data_list):
        """ Compile regex object from the data_list
            It's ok even the data_list is empty

        :param data_list:
        :return: compiled regex object
        """

        # TODO, fix here
        # It is tricky here, since compiled regex from empty list would match anything
        # However, return empty list is not a good idea too
        # try to raise some useful info to let caller decide what to do
        if not data_list:
            return list()

        # re format should be  (expression1|expression2|expression3)$
        data_list_re = f"({'|'.join(data_list)})$"

        compiled_data_list_re = re.compile(data_list_re, re.IGNORECASE)

        return compiled_data_list_re