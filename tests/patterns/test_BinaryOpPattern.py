import operator

import pytest

from supriya.patterns import BinaryOpPattern, SequencePattern
from supriya.patterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, operator, input_a, input_b, expected, is_infinite",
    [
        (None, operator.add, 1, 7, [8], True),
        (None, operator.add, [1], 7, [(8,)], True),
        (None, operator.add, [1], [7], [(8,)], True),
        (None, operator.add, [[1]], [7], [((8,),)], True),
        (None, operator.add, [[[1]]], [7], [(((8,),),)], True),
        (None, operator.add, [1, 2], [7, 8], [(8, 10)], True),
        (None, operator.add, [1, 2], [7, 8, 10], [(8, 10, 11)], True),
        (None, operator.mul, SequencePattern([1, 2, 3]), 4, [4, 8, 12], False),
        (None, operator.mul, SequencePattern([1, 2, 3], None), 4, [4, 8, 12], True),
        (
            None,
            operator.add,
            SequencePattern(["a", "b", "c"]),
            SequencePattern(["1", "2", "3"]),
            ["a1", "b2", "c3"],
            False,
        ),
    ],
)
def test(stop_at, operator, input_a, input_b, expected, is_infinite):
    pattern = BinaryOpPattern(operator, input_a, input_b)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
