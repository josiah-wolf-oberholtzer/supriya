from uuid import UUID

import pytest

from supriya import AddAction
from supriya.newpatterns import (
    CompositeEvent,
    EventPattern,
    FxPattern,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.newpatterns.events import sanitize
from supriya.synthdefs import SynthDefBuilder
from supriya.ugens import FreeVerb, In, Out

with SynthDefBuilder(in_=0, out=0, mix=0.0) as builder:
    in_ = In.ar(bus=builder["in_"], channel_count=2)
    reverb = FreeVerb.ar(source=in_, mix=builder["mix"])
    _ = Out.ar(bus=builder["out"], source=reverb)

synthdef = builder.build()


@pytest.mark.parametrize(
    "inner_pattern, synthdef, release_time, kwargs, expected, is_infinite",
    [
        (
            EventPattern(a=SequencePattern([1, 2])),
            synthdef,
            0.0,
            {},
            [
                CompositeEvent(
                    [
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            add_action=AddAction.ADD_TO_TAIL,
                            synthdef=synthdef,
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000001"),
                    a=1,
                    add_action=AddAction.ADD_TO_HEAD,
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000002"),
                    a=2,
                    add_action=AddAction.ADD_TO_HEAD,
                ),
                CompositeEvent(
                    [NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000000"))]
                ),
            ],
            False,
        ),
        (
            EventPattern(a=SequencePattern([1, 2])),
            synthdef,
            0.5,
            {"mix": 0.25},
            [
                CompositeEvent(
                    [
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            add_action=AddAction.ADD_TO_TAIL,
                            mix=0.25,
                            synthdef=synthdef,
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000001"),
                    a=1,
                    add_action=AddAction.ADD_TO_HEAD,
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000002"),
                    a=2,
                    add_action=AddAction.ADD_TO_HEAD,
                ),
                CompositeEvent(
                    [
                        NullEvent(delta=0.5),
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000000")),
                    ]
                ),
            ],
            False,
        ),
    ],
)
def test(inner_pattern, synthdef, release_time, kwargs, expected, is_infinite):
    pattern = FxPattern(inner_pattern, synthdef, release_time=release_time, **kwargs)
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
