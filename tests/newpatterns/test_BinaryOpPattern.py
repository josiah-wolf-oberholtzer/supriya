import pytest

from supriya.newpatterns import BinaryOpPattern, SequencePattern


@pytest.mark.parametrize(
    "input_a, operator, input_b, expected, is_infinite, arity",
    [
        (1, "+", 7, [8], True, 1),
        ([1], "+", 7, [[8]], True, 1),
        ([1], "+", [7], [[8]], True, 1),
        ([[1]], "+", [7], [[[8]]], True, 1),
        ([[[1]]], "+", [7], [[[[8]]]], True, 1),
        ([1, 2], "+", [7, 8], [[8, 10]], True, 2),
        ([1, 2], "+", [7, 8, 10], [[8, 10, 11]], True, 3),
        (SequencePattern([1, 2, 3]), "*", 4, [4, 8, 12], False, 1),
        (SequencePattern([1, 2, 3], None), "*", 4, [4, 8, 12], True, 1),
    ],
)
def test(input_a, operator, input_b, expected, is_infinite, arity):
    pattern = BinaryOpPattern(input_a, operator, input_b)
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
