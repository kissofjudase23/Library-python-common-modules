import pytest

from ..parser.parser import EmailParser, Tokenizer
from ..parser.exc import ParseError, TokenizeError


class TestEmailParser(object):

    @pytest.mark.parametrize('from_address, expected_nickname, expected_email', [
        pytest.param('Eva Chen <ceo1.ccs@trend.com.tw>',
                     'Eva Chen',
                     'ceo1.ccs@trend.com.tw',
                     id='FAST001'),
        pytest.param('eva_chen@trendmicro.com <ceo2.ccs@trend.com.jp>',
                     'eva_chen@trendmicro.com',
                     'ceo2.ccs@trend.com.jp',
                     id='FAST002'),
        pytest.param('<ceo3.ccs@trend.com.jp>',
                     None,
                     'ceo3.ccs@trend.com.jp',
                     id='FAST003'),
        pytest.param('ceo4.ccs@roadrunner.com',
                     None,
                     'ceo4.ccs@roadrunner.com',
                     id='FAST004'),
    ])
    def test_parse_from_addr_fast(self,
                                  from_address,
                                  expected_nickname,
                                  expected_email):

        actual_nickname, actual_email = EmailParser.parse_addr(from_address)
        assert expected_nickname == actual_nickname
        assert expected_email == actual_email

    @pytest.mark.parametrize('from_address', [
        pytest.param('<ceo.ccs@roadrunner.com', id='TOFT001'),
        pytest.param('ceo.ccs@roadrunner.com>', id='TOFT002'),
        pytest.param('<<ceo.ccs@roadrunner.com>>', id='TOFT003'),
    ])
    def test_parse_from_address_toft(self, from_address):
        _, _ = EmailParser.parse_addr(from_address)

    @pytest.mark.parametrize('from_address', [
        pytest.param(None, id='FET001')
    ])
    def test_parse_from_address_fet(self, from_address):
        with pytest.raises(ParseError):
            _, _ = EmailParser.parse_addr(from_address)

    @pytest.mark.parametrize('email,expected_domain', [
        pytest.param('ceo.ccs@roadrunner.com',
                     'roadrunner.com',
                     id='FAST001'),
        pytest.param('ceo.ccs@not_me@roadrunner.com',
                     'roadrunner.com',
                     id='FAST002'),
        pytest.param('ceo.ccsnot_meroadrunner.com',
                     None,
                     id='FAST003')
    ])
    def test_parse_domain_from_email_fast(self, email, expected_domain):
        actual_domain = EmailParser.parse_domain(email)
        assert expected_domain == actual_domain


class TestTokenizer(object):

    @pytest.mark.parametrize('raw_str,expected_token_list', [
        pytest.param('eva_chen@trendmicro.com',
                     {'eva', 'chen', 'trendmicro', 'com'},
                     id='FAST001'),
        pytest.param('Eva Chen',
                     {'eva', 'chen'},
                     id='FAST002'),
        pytest.param('Eva;Chen#Luby,Lien.Vincent Lee,',
                     {'eva', 'chen', 'luby', 'lien', 'vincent', 'lee'},
                     id='FAST003'),
        pytest.param('(Eva Chen)',
                     {'eva', 'chen'},
                     id='FAST004'),
        pytest.param('[Eva Chen]',
                     {'eva', 'chen'},
                     id='FAST005'),
        pytest.param('{Eva Chen}',
                     {'eva', 'chen'},
                     id='FAST006'),
        pytest.param('Eva_Chen',
                     {'eva', 'chen'},
                     id='FAST007'),
        pytest.param('"Eva_Chen"',
                     {'eva', 'chen'},
                     id='FAST008'),
    ])
    def test_normalized_tokenize_fast(self, raw_str, expected_token_list):
        actual_token_list = Tokenizer.normalized_tokenize(raw_str)
        assert expected_token_list == actual_token_list

    @pytest.mark.parametrize('raw_str', [
        pytest.param(None, id='FET001')
    ])
    def test_normalized_tokenize_fet(self, raw_str):
        with pytest.raises(TokenizeError):
            _ = Tokenizer.normalized_tokenize(raw_str)
