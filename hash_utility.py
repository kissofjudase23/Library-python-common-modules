import hashlib


class HashUtility(object):

    @staticmethod
    def get_normalized_str_sha1(s):
        return hashlib.sha1(s.upper().encode()).hexdigest()

    @staticmethod
    def get_str_sha1(s):
        return hashlib.sha1(s.encode()).hexdigest()

    @staticmethod
    def get_list_sha1(list_):

        sha1_obj = hashlib.sha1()

        for str_ in list_:
            sha1_obj.update(str_.encode())

        return sha1_obj.hexdigest()

    @staticmethod
    def get_normalized_str_sha256(s):
        return hashlib.sha256(s.upper().encode()).hexdigest()

    @staticmethod
    def get_str_sha256(s):
        return hashlib.sha256(s.encode()).hexdigest()
