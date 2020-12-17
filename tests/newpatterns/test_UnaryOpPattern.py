import pytest

from supriya.newpatterns import SequencePattern, UnaryOpPattern


@pytest.mark.parametrize(
    "input_, operator, expected, is_infinite, arity",
    [
        (1, "-", [-1], True, 1),
        ([1], "-", [[-1]], True, 1),
        ([[1]], "-", [[[-1]]], True, 1),
        ([[[1]]], "-", [[[[-1]]]], True, 1),
        ([1, 2], "-", [[-1, -2]], True, 2),
        (SequencePattern([1, 2, 3]), "-", [-1, -2, -3], False, 1),
        (SequencePattern([1, 2, 3], None), "-", [-1, -2, -3], True, 1),
    ],
)
def test(input_, operator, expected, is_infinite, arity):
    pattern = UnaryOpPattern(input_, operator)
    assert pattern.is_infinite == is_infinite
    assert pattern.arity == arity
    iterator = iter(pattern)
    actual = []
    ceased = True
    for _ in range(1000):
        try:
            actual.append(next(iterator))
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        assert actual[: len(expected)] == expected
    else:
        assert actual == expected
