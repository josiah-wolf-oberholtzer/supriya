import pytest

from supriya.newpatterns import RandomPattern


@pytest.mark.parametrize(
    "minimum, maximum, iterations, is_infinite, arity",
    [
        (0.0, 1.0, None, True, 1),
        (0.0, 1.0, 1, False, 1),
        (0.45, 0.55, None, True, 1),
        (0.0, [1.0, 2.0], None, True, 2),
    ],
)
def test(minimum, maximum, iterations, is_infinite, arity):
    pattern = RandomPattern(minimum=minimum, maximum=maximum, iterations=iterations,)
    assert pattern.is_infinite == is_infinite
    assert pattern.arity == arity
    iterator = iter(pattern)
    ceased = True
    actual = []
    for _ in range(1000):
        try:
            actual.append(next(iterator))
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
    else:
        assert len(actual) == iterations
    # TODO: Verify minimum / maximum bounds
    assert len(set(actual)) == len(actual)
