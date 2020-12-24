from uuid import UUID

from supriya.enums import AddAction, CalculationRate


class Event:
    def __init__(self, *, delta=None):
        self.delta = delta


class BusAllocateEvent(Event):
    def __init__(self, uuid: UUID, *, calculation_rate="audio", delta=None):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)


class BusFreeEvent(Event):
    def __init__(self, uuid: UUID, *, delta=None):
        Event.__init__(self, delta=delta)
        self.uuid = uuid


class CompositeEvent(Event):
    def __init__(self, events, *, delta=None):
        Event.__init__(self, delta=delta)
        self.events = events


class GroupAllocateEvent(Event):
    def __init__(self, uuid: UUID, *, add_action=None, delta=None, target_node=None):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node


class NodeFreeEvent(Event):
    def __init__(self, uuid: UUID, *, delta=None):
        Event.__init__(self, delta=delta)
        self.uuid = uuid


class NoteEvent(Event):
    def __init__(
        self,
        uuid: UUID,
        *,
        add_action=None,
        delta=None,
        duration=None,
        synthdef=None,
        target_node=None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.add_action = AddAction.from_expr(add_action)
        self.duration = duration
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def merge(self, event):
        kwargs = self.kwargs.copy()
        kwargs.update(event.kwargs)
        if event.delta is not None:
            kwargs["delta"] = event.delta
        if event.uuid is not None:
            kwargs["uuid"] = event.uuid
        return type(self)(**kwargs)


class NullEvent(Event):
    pass


class SynthAllocateEvent(Event):
    def __init__(
        self,
        uuid: UUID,
        *,
        add_action=None,
        delta=None,
        synthdef=None,
        target_node=None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.add_action = AddAction.from_expr(add_action)
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs
