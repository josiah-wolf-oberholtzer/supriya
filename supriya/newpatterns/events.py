from uuid import UUID

from uqbar.objects import get_repr, get_vars

from supriya.enums import AddAction, CalculationRate


class Event:
    def __init__(self, *, delta=0.0):
        self.delta = delta

    def __eq__(self, expr):
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __repr__(self):
        return get_repr(self, multiline=False)


class BusAllocateEvent(Event):
    def __init__(
        self, uuid: UUID, *, calculation_rate="audio", channel_count=1, delta=0.0
    ):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)
        self.channel_count = channel_count


class BusFreeEvent(Event):
    def __init__(self, uuid: UUID, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.uuid = uuid


class CompositeEvent(Event):
    def __init__(self, events, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.events = events


class GroupAllocateEvent(Event):
    def __init__(
        self,
        uuid: UUID,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
        target_node=None,
    ):
        Event.__init__(self, delta=delta)
        self.uuid = uuid
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node


class NodeFreeEvent(Event):
    def __init__(self, uuid: UUID, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.uuid = uuid


class NoteEvent(Event):
    def __init__(
        self,
        uuid: UUID,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
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
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
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


class MockUUID:
    def __init__(self, string):
        self.string = string

    def __eq__(self, expr):
        self_values = type(self), get_vars(self)
        try:
            expr_values = type(expr), get_vars(expr)
        except AttributeError:
            expr_values = type(expr), expr
        return self_values == expr_values

    def __repr__(self):
        return get_repr(self, multiline=False)


def sanitize_uuid(uuid, cache):
    if uuid not in cache:
        cache[uuid] = MockUUID(chr(len(cache) + 65))
    return cache[uuid]


def sanitize_event(event, cache):
    sanitize_data = {}
    args, _, kwargs = get_vars(event)
    for key, value in args.items():
        if isinstance(value, UUID):
            value = sanitize_uuid(value, cache)
        sanitize_data[key] = value
    for key, value in sorted(kwargs.items()):
        if isinstance(value, UUID):
            value = sanitize_uuid(value, cache)
        sanitize_data[key] = value
    return type(event)(**sanitize_data)


def sanitize(events):
    cache = {}
    sanitized_events = []
    for event in events:
        if isinstance(event, CompositeEvent):
            sanitized_event = CompositeEvent(
                events=[
                    sanitize_event(child_event, cache) for child_event in event.events
                ],
                delta=event.delta,
            )
        else:
            sanitized_event = sanitize_event(event, cache)
        sanitized_events.append(sanitized_event)
    return sanitized_events
