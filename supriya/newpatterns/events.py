from uqbar.objects import get_repr, get_vars, new

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

    def perform(self, provider, mapping):
        pass


class BusAllocateEvent(Event):
    def __init__(self, id_, *, calculation_rate="audio", channel_count=1, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.calculation_rate = CalculationRate.from_expr(calculation_rate)
        self.channel_count = channel_count

    def perform(self, provider, mapping):
        mapping[self.id_] = provider.add_bus_group(
            calculation_rate=self.calculation_rate, channel_count=self.channel_count,
        )


class BusFreeEvent(Event):
    def __init__(self, id_, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(self, provider, mapping):
        mapping[self.id_].free()


class CompositeEvent(Event):
    def __init__(self, events, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.events = events


class GroupAllocateEvent(Event):
    def __init__(
        self, id_, *, add_action=AddAction.ADD_TO_HEAD, delta=0.0, target_node=None,
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.target_node = target_node

    def perform(self, provider, mapping):
        mapping[self.id_] = provider.add_group(
            add_action=self.add_action, target_node=mapping.get(self.target_node),
        )


class NodeFreeEvent(Event):
    def __init__(self, id_, *, delta=0.0):
        Event.__init__(self, delta=delta)
        self.id_ = id_

    def perform(self, provider, mapping):
        mapping[self.id_].free()


class NoteEvent(Event):
    def __init__(
        self,
        id_,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
        duration=None,
        synthdef=None,
        target_node=None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.duration = duration
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def expand(self):
        pass

    def merge(self, event):
        _, _, kwargs = get_vars(event)
        return new(self, **kwargs)

    def perform(self, provider, mapping):
        mapping[self.id_] = provider.add_synth(
            add_action=self.add_action,
            synthdef=self.synthdef,
            target_node=mapping.get(self.target_node),
            **self.kwargs,
        )


class NullEvent(Event):
    pass


class SynthAllocateEvent(Event):
    def __init__(
        self,
        id_,
        *,
        add_action=AddAction.ADD_TO_HEAD,
        delta=0.0,
        synthdef=None,
        target_node=None,
        **kwargs,
    ):
        Event.__init__(self, delta=delta)
        self.id_ = id_
        self.add_action = AddAction.from_expr(add_action)
        self.synthdef = synthdef
        self.target_node = target_node
        self.kwargs = kwargs

    def perform(self, provider, mapping):
        mapping[self.id_] = provider.add_synth(
            add_action=self.add_action,
            synthdef=self.synthdef,
            target_node=mapping.get(self.target_node),
            **self.kwargs,
        )
