from uuid import uuid4


class Event:
    def __init__(self, delta=0, uuid=None, **kwargs):
        self.delta = delta
        self.uuid = uuid or uuid4()
        self.kwargs = kwargs


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
