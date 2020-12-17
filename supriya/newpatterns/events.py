from uuid import uuid4


class Event:
    def __init__(self, delta=None, uuid=None, **kwargs):
        self.delta = delta
        self.uuid = uuid or uuid4()
        self.kwargs = kwargs

    def merge(self, event):
        kwargs = self.kwargs.copy()
        kwargs.update(event.kwargs)
        if event.delta is not None:
            kwargs["delta"] = event.delta
        if event.uuid is not None:
            kwargs["uuid"] = event.uuid
        return type(self)(**kwargs)


class BusAllocateEvent(Event):
    pass


class BusFreeEvent(Event):
    pass


class GroupAllocateEvent(Event):
    pass


class GroupFreeEvent(Event):
    pass


class NoteEvent(Event):
    pass


class CompositeEvent(Event):
    pass
