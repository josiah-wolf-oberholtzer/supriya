from uuid import UUID

import pytest

from supriya import AddAction
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
from supriya.newpatterns.events import sanitize


@pytest.mark.parametrize(
    "inner_pattern, release_time, expected, is_infinite",
    [
        (
            EventPattern(a=SequencePattern([1, 2])),
            0.0,
            [
                CompositeEvent(
                    [
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            add_action=AddAction.ADD_TO_HEAD,
                            delta=0.0,
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000001"),
                    a=1,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=UUID("00000000-0000-0000-0000-000000000000"),
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000002"),
                    a=2,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=UUID("00000000-0000-0000-0000-000000000000"),
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(
                            UUID("00000000-0000-0000-0000-000000000000"), delta=0.0
                        ),
                    ]
                ),
            ],
            False,
        ),
        (
            EventPattern(a=SequencePattern([1, 2])),
            0.25,
            [
                CompositeEvent(
                    [
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            add_action=AddAction.ADD_TO_HEAD,
                            delta=0.0,
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000001"),
                    a=1,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=UUID("00000000-0000-0000-0000-000000000000"),
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000002"),
                    a=2,
                    add_action=AddAction.ADD_TO_HEAD,
                    target_node=UUID("00000000-0000-0000-0000-000000000000"),
                ),
                CompositeEvent(
                    [
                        NullEvent(delta=0.25),
                        NodeFreeEvent(
                            UUID("00000000-0000-0000-0000-000000000000"), delta=0.0
                        ),
                    ]
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
