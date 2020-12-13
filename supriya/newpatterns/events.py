class Event:
    def __init__(self, **kwargs):
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


class RestEvent(Event):
    pass


class CompositeEvent(Event):
    pass
