import easy_pysy as ez


def test_chaining():
    arr = [1, 2, 3, 4, 5, 6]
    result = ez.magic(arr)\
        .map(lambda v: v * 2)\
        .filter(lambda v: v % 2 == 0)
    assert result == [2, 4, 6, 8, 10, 12]
