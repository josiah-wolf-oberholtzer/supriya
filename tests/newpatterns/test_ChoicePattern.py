import pytest
from uqbar.iterables import nwise

from supriya.newpatterns import ChoicePattern, SequencePattern


@pytest.mark.parametrize(
    "sequence, iterations, forbid_repetitions, weights, is_infinite, arity",
    [
        ([1, 2, 3], 1, False, None, False, 1),
        ([1, 2, 3], 1, True, None, False, 1),
        ([1, 2, 3], None, False, None, True, 1),
        ([1, 2, 3], None, True, None, True, 1),
        ([1, 2, 3], None, True, [1, 2, 1], True, 1),
        (
            [SequencePattern(["a", "b"]), SequencePattern(["c", "d"])],
            None,
            False,
            None,
            True,
            1,
        ),
    ],
)
def test(sequence, iterations, forbid_repetitions, weights, is_infinite, arity):
    pattern = ChoicePattern(
        sequence,
        iterations=iterations,
        forbid_repetitions=forbid_repetitions,
        weights=weights,
    )
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
    if forbid_repetitions:
        for a, b in nwise(actual):
            assert a != b
