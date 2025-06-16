from pytest import raises

from src.app.utils import CollectionUtils


def test_is_empty():
    assert CollectionUtils.is_empty([])
    assert not CollectionUtils.is_empty([None])
    assert not CollectionUtils.is_empty({1, })
    test_data = None
    with raises(TypeError, match=f"输入的参数需为 Collection 类型, {test_data} 为 {type(test_data)}"):
        CollectionUtils.is_empty(test_data)
