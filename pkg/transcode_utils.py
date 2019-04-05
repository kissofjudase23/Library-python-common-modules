import base64


class TransCoder(object):
    @staticmethod
    def decode_base64(b64str, *, encoding='utf-8'):
        if not b64str:
            return

        return base64.b64decode(b64str).decode(encoding)

    @staticmethod
    def lazy_decode_base64(b64str, *, encoding='utf-8'):
        if not b64str:
            return None
        try:
            return base64.b64decode(b64str).decode(encoding)
        except Exception:
            return None

    @staticmethod
    def encode_base64(str_, *, encoding='utf-8'):
        if not str_:
            return

        return base64.b64encode(bytes(str_, encoding)).decode(encoding)