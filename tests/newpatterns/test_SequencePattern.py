import pytest

from supriya.newpatterns import SequencePattern


@pytest.mark.parametrize(
    "sequence, iterations, expected, is_infinite, arity",
    [
        ([1, 2, 3], None, [1, 2, 3], True, 1),
        ([1, 2, 3], 1, [1, 2, 3], False, 1),
        ([1, 2, 3], 2, [1, 2, 3, 1, 2, 3], False, 1),
        ([1, 2, 3, SequencePattern(["a", "b"])], 1, [1, 2, 3, "a", "b"], False, 1),
        ([1, 2, 3, SequencePattern(["a", "b"], None)], 1, [1, 2, 3, "a", "b"], True, 1),
        (
            [SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])],
            1,
            [1, 2, 3, "a", "b"],
            False,
            1,
        ),
        (
            [SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])],
            2,
            [1, 2, 3, "a", "b", 1, 2, 3, "a", "b"],
            False,
            1,
        ),
        (
            [SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])],
            1,
            [1, 2, 3],
            True,
            1,
        ),
        (
            [SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])],
            None,
            [1, 2, 3],
            True,
            1,
        ),
    ],
)
def test(sequence, iterations, expected, is_infinite, arity):
    pattern = SequencePattern(sequence, iterations=iterations)
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
