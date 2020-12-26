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
from supriya.newpatterns.testutils import MockUUID as M
from supriya.newpatterns.testutils import run_pattern_test


@pytest.mark.parametrize(
    "stop_at, patterns, expected, is_infinite",
    [
        (
            None,
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
            None,
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
def test(stop_at, patterns, expected, is_infinite):
    pattern = ParallelPattern(patterns)
    run_pattern_test(pattern, expected, is_infinite, stop_at)
