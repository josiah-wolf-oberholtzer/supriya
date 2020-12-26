from uuid import UUID

import pytest

from supriya.newpatterns import (
    EventPattern,
    NoteEvent,
    ParallelPattern,
    SequencePattern,
)
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
                NoteEvent(UUID("00000000-0000-0000-0000-000000000000"), x=1),
                NoteEvent(UUID("00000000-0000-0000-0000-000000000001"), delta=1.0, y=1),
                NoteEvent(UUID("00000000-0000-0000-0000-000000000002"), delta=0.5, x=2),
                NoteEvent(UUID("00000000-0000-0000-0000-000000000003"), delta=0.5, y=2),
                NoteEvent(UUID("00000000-0000-0000-0000-000000000004"), delta=1.0, x=3),
            ],
            False,
        )
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
        assert sanitize(actual) == expected
