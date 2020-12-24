from uuid import uuid4

from supriya.enums import CalculationRate

from .events import (
    CompositeEvent,
    GroupAllocateEvent,
    NodeFreeEvent,
    NullEvent,
)
from .patterns import Pattern


class BusPattern(Pattern):
    def __init__(
        self,
        pattern,
        calculation_rate="AUDIO",
        channel_count=1,
        release_time=0.25,
        in_parameter_name="in_",
        out_parameter_name="out",
    ):
        self._pattern = pattern
        self._calculation_rate = CalculationRate.from_expr(calculation_rate)
        self._channel_count = channel_count
        self._release_time = release_time


class FxPattern(Pattern):
    def __init__(self, pattern, synthdef, **kwargs):
        pass


class GroupPattern(Pattern):
    def __init__(self, pattern, release_time=0.25):
        self._pattern = pattern
        self._release_time = release_time

    def _setup_peripherals(self, state):
        uuid = state["group_uuid"]
        starts = [GroupAllocateEvent(add_action="ADD_TO_HEAD", uuid=uuid)]
        stops = [NodeFreeEvent(uuid=uuid)]
        if self.release_time:
            stops.insert(0, NullEvent(delta=self.release_time))
        return CompositeEvent(starts), CompositeEvent(stops)

    def _setup_state(self):
        return {"group_uuid": uuid4()}


class ParallelPattern(Pattern):
    def __init__(self, patterns, *, with_groups=False):
        pass
