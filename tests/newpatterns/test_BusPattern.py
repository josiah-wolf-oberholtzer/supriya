from uuid import UUID

import pytest

from supriya import AddAction, CalculationRate
from supriya.assets import synthdefs
from supriya.newpatterns import (
    BusAllocateEvent,
    BusFreeEvent,
    BusPattern,
    CompositeEvent,
    EventPattern,
    GroupAllocateEvent,
    NodeFreeEvent,
    NoteEvent,
    NullEvent,
    SequencePattern,
    SynthAllocateEvent,
)
from supriya.newpatterns.events import sanitize


@pytest.mark.parametrize(
    "inner_pattern, calculation_rate, channel_count, release_time, expected, is_infinite",
    [
        (
            EventPattern(a=SequencePattern([1, 2])),
            "audio",
            2,
            0.0,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000002"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.0,
                            in_=UUID("00000000-0000-0000-0000-000000000000"),
                            synthdef=synthdefs.system_link_audio_2,
                            target_node=UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000003"),
                    a=1,
                    out=UUID("00000000-0000-0000-0000-000000000000"),
                    target_node=UUID("00000000-0000-0000-0000-000000000001"),
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000004"),
                    a=2,
                    out=UUID("00000000-0000-0000-0000-000000000000"),
                    target_node=UUID("00000000-0000-0000-0000-000000000001"),
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000002")),
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000001")),
                        BusFreeEvent(UUID("00000000-0000-0000-0000-000000000000")),
                    ]
                ),
            ],
            False,
        ),
        (
            EventPattern(a=SequencePattern([1, 2])),
            "audio",
            2,
            0.25,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000002"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID("00000000-0000-0000-0000-000000000000"),
                            synthdef=synthdefs.system_link_audio_2,
                            target_node=UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000003"),
                    a=1,
                    out=UUID("00000000-0000-0000-0000-000000000000"),
                    target_node=UUID("00000000-0000-0000-0000-000000000001"),
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000004"),
                    a=2,
                    out=UUID("00000000-0000-0000-0000-000000000000"),
                    target_node=UUID("00000000-0000-0000-0000-000000000001"),
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000002")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000001")),
                        BusFreeEvent(UUID("00000000-0000-0000-0000-000000000000")),
                    ]
                ),
            ],
            False,
        ),
        (
            BusPattern(EventPattern(a=SequencePattern([1, 2])), channel_count=2),
            "audio",
            2,
            0.25,
            [
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000000"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000002"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID("00000000-0000-0000-0000-000000000000"),
                            synthdef=synthdefs.system_link_audio_2,
                            target_node=UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                    ]
                ),
                CompositeEvent(
                    [
                        BusAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000003"),
                            calculation_rate=CalculationRate.AUDIO,
                            channel_count=2,
                        ),
                        GroupAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000004"),
                            target_node=UUID("00000000-0000-0000-0000-000000000001"),
                        ),
                        SynthAllocateEvent(
                            UUID("00000000-0000-0000-0000-000000000005"),
                            add_action=AddAction.ADD_AFTER,
                            amplitude=1.0,
                            fade_time=0.25,
                            in_=UUID("00000000-0000-0000-0000-000000000003"),
                            out=UUID("00000000-0000-0000-0000-000000000000"),
                            synthdef=synthdefs.system_link_audio_2,
                            target_node=UUID("00000000-0000-0000-0000-000000000004"),
                        ),
                    ]
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000006"),
                    a=1,
                    out=UUID("00000000-0000-0000-0000-000000000003"),
                    target_node=UUID("00000000-0000-0000-0000-000000000004"),
                ),
                NoteEvent(
                    UUID("00000000-0000-0000-0000-000000000007"),
                    a=2,
                    out=UUID("00000000-0000-0000-0000-000000000003"),
                    target_node=UUID("00000000-0000-0000-0000-000000000004"),
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000005")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000004")),
                        BusFreeEvent(UUID("00000000-0000-0000-0000-000000000003")),
                    ]
                ),
                CompositeEvent(
                    [
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000002")),
                        NullEvent(delta=0.25),
                        NodeFreeEvent(UUID("00000000-0000-0000-0000-000000000001")),
                        BusFreeEvent(UUID("00000000-0000-0000-0000-000000000000")),
                    ]
                ),
            ],
            False,
        ),
    ],
)
def test(
    inner_pattern, calculation_rate, channel_count, release_time, expected, is_infinite
):
    pattern = BusPattern(
        inner_pattern,
        calculation_rate=calculation_rate,
        channel_count=channel_count,
        release_time=release_time,
    )
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
