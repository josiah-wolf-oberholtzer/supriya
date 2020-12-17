import pytest

from supriya.newpatterns import EventPattern, NoteEvent, SequencePattern


@pytest.mark.parametrize(
    "input_a, input_b, expected, is_infinite, arity",
    [
        (
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], None),
            [
                {"a": 1, "b": 4},
                {"a": 2, "b": 5},
                {"a": 3, "b": 4},
                {"a": 1, "b": 5},
                {"a": 2, "b": 4},
                {"a": 3, "b": 5},
            ],
            True,
            1,
        ),
        (
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 1),
            [{"a": 1, "b": 4}, {"a": 2, "b": 5}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], None),
            SequencePattern([4, 5], 2),
            [{"a": 1, "b": 4}, {"a": 2, "b": 5}, {"a": 3, "b": 4}, {"a": 1, "b": 5}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], 1),
            [{"a": 1, "b": 4}, {"a": 2, "b": 5}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], 1),
            SequencePattern([4, 5], None),
            [{"a": 1, "b": 4}, {"a": 2, "b": 5}, {"a": 3, "b": 4}],
            False,
            1,
        ),
        (
            SequencePattern([1, 2, 3], 1),
            4,
            [{"a": 1, "b": 4}, {"a": 2, "b": 4}, {"a": 3, "b": 4}],
            False,
            1,
        ),
    ],
)
def test(input_a, input_b, expected, is_infinite, arity):
    pattern = EventPattern(a=input_a, b=input_b,)
    assert pattern.is_infinite == is_infinite
    assert pattern.arity == arity
    iterator = iter(pattern)
    actual = []
    ceased = True
    uuids = set()
    for iteration in range(1000):
        try:
            event = next(iterator)
            assert isinstance(event, NoteEvent)
            uuids.add(event.uuid)
            actual.append(event.kwargs)
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        assert actual[: len(expected)] == expected
        assert len(uuids) == 1000
    else:
        assert actual == expected
        assert len(uuids) == iteration
