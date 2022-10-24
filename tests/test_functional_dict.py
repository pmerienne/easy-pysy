import easy_pysy as ez


def test_chaining():
    dick = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
    result = ez.magic(dick)\
        .keep(lambda k, v: k % 2 == 0)\
        .omit(lambda k, v: v > 45)
    assert result == {2: 20, 4: 40}

