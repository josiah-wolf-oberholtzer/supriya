import pytest

from supriya.newpatterns import BinaryOpPattern, SequencePattern


@pytest.mark.parametrize(
    "input_a, operator, input_b, expected, is_infinite",
    [
        (1, "+", 7, [8], True),
        ([1], "+", 7, [[8]], True),
        ([1], "+", [7], [[8]], True),
        ([[1]], "+", [7], [[[8]]], True),
        ([[[1]]], "+", [7], [[[[8]]]], True),
        ([1, 2], "+", [7, 8], [[8, 10]], True),
        ([1, 2], "+", [7, 8, 10], [[8, 10, 11]], True),
        (SequencePattern([1, 2, 3]), "*", 4, [4, 8, 12], False),
        (SequencePattern([1, 2, 3], None), "*", 4, [4, 8, 12], True),
    ],
)
def test(input_a, operator, input_b, expected, is_infinite):
    pattern = BinaryOpPattern(input_a, operator, input_b)
    assert pattern.is_infinite == is_infinite
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
