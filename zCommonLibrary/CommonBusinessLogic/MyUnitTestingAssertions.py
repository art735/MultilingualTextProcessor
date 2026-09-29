def assert_equal(a, b, msg=''):
    assert a == b, f"{msg}: expected {b}, actual {a}"


def assert_raises(exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        assert False, f"Expected exception {exception.__name__}, but it was not raised."
    except exception:
        pass
    # assert True