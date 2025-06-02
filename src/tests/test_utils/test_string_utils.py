import pytest

from src.app.utils import StringUtils


def test_is_any_blank():
    assert StringUtils.is_any_blank('', "asd", "222")
    assert StringUtils.is_any_blank('\n', "asd", "222")
    assert not StringUtils.is_any_blank('1', "asd", "222")
    with pytest.raises(TypeError, match=f"输入的参数需为 str 类型, {123} 为 {type(123)}"):
        StringUtils.is_any_blank("asd", "222", 123)
    with pytest.raises(TypeError, match=f"输入的参数需为 str 类型, {None} 为 {type(None)}"):
        StringUtils.is_any_blank("asd", "222", None)
