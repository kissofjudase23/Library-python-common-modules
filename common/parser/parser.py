import re

import nltk

from .exc import ParseError, TokenizeError


class EmailParser(object):

    COMPILED_ADDR_REGEX = re.compile(r'(.*)<(.*@.*)>', re.IGNORECASE)

    @classmethod
    def parse_addr(cls, address):
        """
        :param address:
            case1: Eva Chen <ceo1.ccs@trend.com.tw>
            case2: eva_chen@trendmicro.com <ceo2.ccs@trend.com.jp>
            case3: <ceo3.ccs@trend.com.jp>
            case4: ceo4.ccs@roadrunner.com
        :return:
            case1:
                nickname: Eva Chen
                email: ceo1.ccs@trend.com.tw
            case2:
                nickname: eva_chen@trendmicro.com
                email: ceo2.ccs@trend.com.jp
            case3:
                nickname: None
                email: ceo3.ccs@trend.com.jp
            case4:
                nickname: None
                email: ceo4.ccs@trend.com.jp
        :raises:
            ParseError
        """
        try:

            matches = cls.COMPILED_ADDR_REGEX.search(address)

            # case1,2,3
            if matches:
                nickname = matches.group(1).lstrip().rstrip()
                email = matches.group(2).lstrip().rstrip()
            # case4
            else:
                nickname = None
                email = address.lstrip().rstrip()

            if nickname == '':
                nickname = None

            return nickname, email

        except Exception as e:
            raise ParseError(f'parse nickname, domain error, e:{e}') from e

    @staticmethod
    def parse_domain(email):
        """
        :param email:
            case1: havedomain@trend.com.tw
            case2: nodomain
        :return:
           domain:
            case1: trend.com.tw
            case2: None
        :raises:
            ParseError
        """
        try:
            at_position = email.rfind('@')
            if at_position is -1:
                return None

            else:
                domain = email[at_position + 1:]
            return domain

        except Exception as e:
            raise ParseError(f'parse domain error, e:{e}') from e


class Tokenizer(object):
    @staticmethod
    def tokenize(raw_str):
        """
        :param raw_str:
            case1:
                '  [case1] :case2: #case3# ,case4, {case5}'
        :return:
            case1:
                ['[', 'case1', ']', ':', 'case2', ':', '#', 'case3', '#', ',', 'case4', ',', '{', 'case5', '}']
        :raises:
            TokenizeError
        """
        try:
            return nltk.wordpunct_tokenize(raw_str)
        except Exception as e:
            raise TokenizeError('tokenize error, e:{e}') from e

    @staticmethod
    def normalized_tokenize(raw_str):
        """
            Lower the tokens, and purge the token with length is 1
            support 'whitespace' ';' '#'  ',' '(' ')' '[' ']' '_'
        :param raw_str:
            case1:
                'eva_chen@trendmicro.com'
        :return:
            case1:
                {'eva', 'chen', 'trendmicro', 'com'}
        :raises:
            TokenizeError
        """
        tokenized_result = Tokenizer.tokenize(raw_str)

        normalized_tokens = {token.lower() for token in tokenized_result if len(token) > 1}

        # special handling for '_'
        for token in normalized_tokens.copy():
            if '_' in token:
                normalized_tokens.remove(token)
                normalized_tokens.update(token.split('_'))

        return normalized_tokens
