import pytest

from supriya.newpatterns import SequencePattern, UnaryOpPattern


@pytest.mark.parametrize(
    "input_, operator, expected, is_infinite",
    [
        (1, "-", [-1], True),
        ([1], "-", [[-1]], True),
        ([[1]], "-", [[[-1]]], True),
        ([[[1]]], "-", [[[[-1]]]], True),
        ([1, 2], "-", [[-1, -2]], True),
        (SequencePattern([1, 2, 3]), "-", [-1, -2, -3], False),
        (SequencePattern([1, 2, 3], None), "-", [-1, -2, -3], True),
    ],
)
def test(input_, operator, expected, is_infinite):
    pattern = UnaryOpPattern(input_, operator)
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
