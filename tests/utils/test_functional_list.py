import easy_pysy as ez


def test_chaining():
    arr = [1, 2, 3, 4, 5, 6]
    result = ez.magic(arr) \
        .map(lambda v: v * 2) \
        .filter(lambda v: v % 2 == 0)
    assert result == [2, 4, 6, 8, 10, 12]


def test_support_any_iterable():
    assert ez.magic(range(10)) \
               .filter(lambda v: v > 3) \
               .find(lambda v: v % 2 == 0) == 4
