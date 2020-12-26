import pytest

from supriya.newpatterns import (
    CompositeEvent,
    EventPattern,
    GroupAllocateEvent,
    GroupPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
)
from supriya.newpatterns.events import MockUUID as M
from supriya.newpatterns.events import sanitize


@pytest.mark.parametrize(
    "inner_pattern, release_time, expected, is_infinite",
    [
        (
            EventPattern(a=SequencePattern([1, 2])),
            0.0,
            [
                CompositeEvent([GroupAllocateEvent(M("A"), delta=0.0)]),
                NoteEvent(M("B"), a=1, target_node=M("A"),),
                NoteEvent(M("C"), a=2, target_node=M("A"),),
                CompositeEvent([NodeFreeEvent(M("A"), delta=0.0)]),
            ],
            False,
        ),
        (
            EventPattern(a=SequencePattern([1, 2])),
            0.25,
            [
                CompositeEvent([GroupAllocateEvent(M("A"), delta=0.0)]),
                NoteEvent(M("B"), a=1, target_node=M("A"),),
                NoteEvent(M("C"), a=2, target_node=M("A"),),
                CompositeEvent(
                    [NullEvent(delta=0.25), NodeFreeEvent(M("A"), delta=0.0)]
                ),
            ],
            False,
        ),
    ],
)
def test(inner_pattern, release_time, expected, is_infinite):
    pattern = GroupPattern(inner_pattern, release_time=release_time)
    assert pattern.is_infinite == is_infinite
    iterator = iter(pattern)
    actual = []
    ceased = True
    for iteration in range(1000):
        try:
            event = next(iterator)
            actual.append(event)
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        assert sanitize(actual[: len(expected)]) == expected
    else:
        assert sanitize(actual) == expected
