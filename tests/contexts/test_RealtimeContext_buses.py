import asyncio
import logging

import pytest
import pytest_asyncio

from supriya import default
from supriya.contexts.core import InvalidCalculationRate
from supriya.contexts.realtime import AsyncServer, Server
from supriya.osc import OscMessage


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request):
    context = request.param()
    await get(context.boot())
    context.add_synthdefs(default)
    await get(context.sync())
    yield context


@pytest.mark.asyncio
async def test_Bus_allocated(context):
    # TODO: what are the semantics actually?
    #       buses always exist.
    #       but the /leasing/ of a bus ID is temporal.
    #       what we need is a distinction between the permanent...
    #       ... and the leased.
    audio_bus = context.add_bus("AUDIO")
    control_bus = context.add_bus("CONTROL")
    assert audio_bus.allocated
    assert control_bus.allocated
    audio_bus.free()
    control_bus.free()
    assert audio_bus.allocated
    assert control_bus.allocated
    await get(context.quit())
    assert not audio_bus.allocated
    assert not control_bus.allocated


@pytest.mark.asyncio
async def test_add_bus(context):
    # invalid calculation rate
    with pytest.raises(InvalidCalculationRate):
        context.add_bus("SCALAR")
    # ok
    with context.osc_protocol.capture() as transcript:
        audio_bus = context.add_bus("AUDIO")
        control_bus = context.add_bus("CONTROL")
    assert audio_bus.context is context
    assert audio_bus.id_ == 16
    assert control_bus.context is context
    assert control_bus.id_ == 0
    assert transcript.filtered(received=False, status=False) == []


@pytest.mark.asyncio
async def test_add_bus_group(context):
    # invalid calculation rate
    with pytest.raises(InvalidCalculationRate):
        context.add_bus_group("SCALAR")
    # count less than 1
    with pytest.raises(ValueError):
        context.add_bus_group("AUDIO", 0)
    # ok
    with context.osc_protocol.capture() as transcript:
        audio_bus_group = context.add_bus_group("AUDIO", 8)
        control_bus_group = context.add_bus_group("CONTROL", 4)
    assert len(audio_bus_group) == 8
    assert all(audio_bus.context is context for audio_bus in audio_bus_group)
    assert [audio_bus.id_ for audio_bus in audio_bus_group] == [
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
    ]
    assert len(control_bus_group) == 4
    assert all(control_bus.context is context for control_bus in control_bus_group)
    assert [control_bus.id_ for control_bus in control_bus_group] == [0, 1, 2, 3]
    assert transcript.filtered(received=False, status=False) == []


@pytest.mark.asyncio
async def test_fill_buses(context):
    audio_bus = context.add_bus("AUDIO")
    control_bus_a = context.add_bus("CONTROL")
    control_bus_b = context.add_bus("CONTROL")
    control_bus_c = context.add_bus("CONTROL")
    with context.osc_protocol.capture() as transcript:
        with pytest.raises(InvalidCalculationRate):
            audio_bus.fill(2, 0.75)
        control_bus_a.fill(3, 0.5)
        with context.at():
            control_bus_b.fill(4, 0.25)
            control_bus_c.fill(5, 0.125)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/c_fill", 0, 3, 0.5),
        OscMessage("/c_fill", 1, 4, 0.25, 2, 5, 0.125),
    ]


@pytest.mark.asyncio
async def test_free_bus(context):
    audio_bus = context.add_bus("AUDIO")
    control_bus = context.add_bus("CONTROL")
    with context.osc_protocol.capture() as transcript:
        audio_bus.free()
        control_bus.free()
    assert transcript.filtered(received=False, status=False) == []
    new_audio_bus = context.add_bus("AUDIO")
    new_control_bus = context.add_bus("CONTROL")
    # verify IDs are re-used
    assert audio_bus.id_ == new_audio_bus.id_
    assert control_bus.id_ == new_control_bus.id_


@pytest.mark.asyncio
async def test_set_bus(context):
    audio_bus = context.add_bus("AUDIO")
    control_bus_a = context.add_bus("CONTROL")
    control_bus_b = context.add_bus("CONTROL")
    control_bus_c = context.add_bus("CONTROL")
    with context.osc_protocol.capture() as transcript:
        with pytest.raises(InvalidCalculationRate):
            audio_bus.set_(0.75)
        control_bus_a.set_(0.5)
        with context.at():
            control_bus_b.set_(0.25)
            control_bus_c.set_(0.125)
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/c_set", 0, 0.5),
        OscMessage("/c_set", 1, 0.25, 2, 0.125),
    ]
