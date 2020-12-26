import pytest

from supriya.newpatterns import (
    CompositeEvent,
    EventPattern,
    GroupAllocateEvent,
    GroupPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    ParallelPattern,
    SequencePattern,
)
from supriya.newpatterns.events import MockUUID as M
from supriya.newpatterns.events import sanitize


@pytest.mark.parametrize(
    "patterns, expected, is_infinite",
    [
        (
            [
                EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0),
                EventPattern(y=SequencePattern([1, 2]), delta=1.5),
            ],
            [
                NoteEvent(M("A"), x=1),
                NoteEvent(M("B"), delta=1.0, y=1),
                NoteEvent(M("C"), delta=0.5, x=2),
                NoteEvent(M("D"), delta=0.5, y=2),
                NoteEvent(M("E"), delta=1.0, x=3),
            ],
            False,
        ),
        (
            [
                GroupPattern(EventPattern(x=SequencePattern([1, 2, 3]), delta=1.0)),
                GroupPattern(EventPattern(y=SequencePattern([1, 2]), delta=1.5)),
            ],
            [
                CompositeEvent([GroupAllocateEvent(M("A"))]),
                CompositeEvent([GroupAllocateEvent(M("B"))]),
                NoteEvent(M("C"), target_node=M("A"), x=1,),
                NoteEvent(M("D"), delta=1.0, target_node=M("B"), y=1,),
                NoteEvent(M("E"), delta=0.5, target_node=M("A"), x=2,),
                NoteEvent(M("F"), delta=0.5, target_node=M("B"), y=2,),
                NoteEvent(M("G"), delta=1.0, target_node=M("A"), x=3,),
                CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(M("A"))]),
                CompositeEvent([NullEvent(delta=0.25), NodeFreeEvent(M("B"))]),
            ],
            False,
        ),
    ],
)
def test(patterns, expected, is_infinite):
    pattern = ParallelPattern(patterns)
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
        for x in sanitize(actual):
            print(x)
        assert sanitize(actual) == expected
