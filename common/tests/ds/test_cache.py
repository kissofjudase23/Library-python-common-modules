import pytest

from ...ds.cache import LRUCache


class TestLRUCache(object):

    @pytest.mark.parametrize('cap, datas, expected, expected_len', [
        pytest.param(3, {"a": 100, "b": 200, "c": 300},
                     "c:300<->b:200<->a:100", 3),
        pytest.param(2, {"a": 100, "b": 200, "c": 300},
                     "c:300<->b:200", 2),
        pytest.param(1, {"a": 100, "b": 200, "c": 300},
                     "c:300", 1),
    ])
    def test_cache_capacity(self, cap, datas, expected, expected_len):
        cache = LRUCache(cap)

        for k, v in datas.items():
            cache.set(k, v)

        assert repr(cache) == expected
        assert cache.len == expected_len

    def test_cache_delete(self):
        cache = LRUCache(100)

        for k, v in {"a": 100, "b": 200, "c": 300}.items():
            cache.set(k, v)

        assert repr(cache) == "c:300<->b:200<->a:100"
        cache.delete("b")
        assert repr(cache) == "c:300<->a:100"
        cache.delete("c")
        assert repr(cache) == "a:100"
        cache.delete("a")
        assert repr(cache) == ""

    def test_cache_get(self):
        cache = LRUCache(100)

        d = {"a": 100, "b": 200, "c": 300}

        for k, v in d.items():
            cache.set(k, v)

        assert repr(cache) == "c:300<->b:200<->a:100"

        assert cache.get("a") == d["a"]
        assert repr(cache) == "a:100<->c:300<->b:200"

        assert cache.get("b") == d["b"]
        assert repr(cache) == "b:200<->a:100<->c:300"

        assert cache.get("a") == d["a"]
        assert repr(cache) == "a:100<->b:200<->c:300"

        assert cache.get("c") == d["c"]
        assert repr(cache) == "c:300<->a:100<->b:200"
