import pytest
from tests.utils import assert_is_dict_contain_dict


def test_is_dict_contain_dict():
    dict1 = {"a": 1, "c": {"d": 3, "e": 4}, "b": [1, 2, 3]}
    dict2 = {"a": 1, "c": {"e": 4}}
    dict3 = {"a": 2, "c": {"d": 3, "e": 4}}
    dict4 = {"a": 2, "c": {"d": 3, "e": 4, "f": 5}}
    dict5 = {"a": 2, "c": {"d": 3, "e": {"f": 5}}}
    dict6 = {"a": 1}
    dict7 = {"a": 1, "c": {"d": 3, "e": 4}}
    dict8 = {"a": 1, "c": {"d": 3, "e": 4}, "b": [1, 2]}
    dict9 = {"a": 1, "c": {"d": 3, "e": 4}, "b": [1, 2, 3, 4]}
    assert_is_dict_contain_dict(dict1, dict2)
    with pytest.raises(RuntimeError):
        assert_is_dict_contain_dict(dict1, dict3)
    with pytest.raises(RuntimeError):
        assert_is_dict_contain_dict(dict1, dict4)
    with pytest.raises(RuntimeError):
        assert_is_dict_contain_dict(dict1, dict5)
    assert_is_dict_contain_dict(dict1, dict6)
    assert_is_dict_contain_dict(dict1, dict7)
    assert_is_dict_contain_dict(dict1, dict8)
    with pytest.raises(RuntimeError):
        assert_is_dict_contain_dict(dict1, dict9)
