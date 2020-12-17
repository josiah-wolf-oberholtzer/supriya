import pytest

from supriya.newpatterns import (
    EventPattern,
    NoteEvent,
    SequencePattern,
    UpdatePattern,
)


@pytest.mark.parametrize(
    "input_a, input_b1, input_b2, input_c, expected, is_infinite, arity",
    [
        (
            SequencePattern([1, 2, 3]),
            SequencePattern([4, 5]),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [{"a": 1, "b": 7, "c": 10}, {"a": 2, "b": 8, "c": 11}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9]),
            SequencePattern([10, 11]),
            [{"a": 1, "b": 7, "c": 10}, {"a": 2, "b": 8, "c": 11}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            SequencePattern([7, 8, 9], None),
            SequencePattern([10, 11], None),
            [
                {"a": 1, "b": 7, "c": 10},
                {"a": 2, "b": 8, "c": 11},
                {"a": 3, "b": 9, "c": 10},
                {"a": 1, "b": 7, "c": 11},
                {"a": 2, "b": 8, "c": 10},
                {"a": 3, "b": 9, "c": 11},
            ],
            True,
            1,
        ),
    ],
)
def test(input_a, input_b1, input_b2, input_c, expected, is_infinite, arity):
    pattern = UpdatePattern(
        EventPattern(a=input_a, b=input_b1,), b=input_b2, c=input_c,
    )
    assert pattern.is_infinite == is_infinite
    assert pattern.arity == arity
    iterator = iter(pattern)
    actual = []
    ceased = True
    for iteration in range(1000):
        try:
            event = next(iterator)
            assert isinstance(event, NoteEvent)
            actual.append(event.kwargs)
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        assert actual[: len(expected)] == expected
    else:
        assert actual == expected
