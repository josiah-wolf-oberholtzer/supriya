import pytest

from supriya.newpatterns import SequencePattern


@pytest.mark.parametrize(
    "sequence, iterations, expected, is_infinite",
    [
        ([1, 2, 3], None, [1, 2, 3], True),
        ([1, 2, 3], 1, [1, 2, 3], False),
        ([1, 2, 3], 2, [1, 2, 3, 1, 2, 3], False),
        ([1, 2, 3, SequencePattern(["a", "b"])], 1, [1, 2, 3, "a", "b"], False),
        ([1, 2, 3, SequencePattern(["a", "b"], None)], 1, [1, 2, 3, "a", "b"], True),
        ([SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])], 1, [1, 2, 3, "a", "b"], False),
        ([SequencePattern([1, 2, 3]), SequencePattern(["a", "b"])], 2, [1, 2, 3, "a", "b", 1, 2, 3, "a", "b"], False),
        ([SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])], 1, [1, 2, 3], True),
        ([SequencePattern([1, 2, 3], None), SequencePattern(["a", "b"])], None, [1, 2, 3], True),
    ],
)
def test(sequence, iterations, expected, is_infinite):
    pattern = SequencePattern(sequence, iterations=iterations)
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
        assert actual[:len(expected)] == expected
    else:
        assert actual == expected
