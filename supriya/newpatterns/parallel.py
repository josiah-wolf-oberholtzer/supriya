from collections import deque
from queue import PriorityQueue

from uqbar.objects import new

from .patterns import Pattern


class ParallelPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, patterns):
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        should_stop = False
        event_queue = deque()
        iterator_queue = PriorityQueue()
        for index, pattern in enumerate(self._patterns):
            iterator = iter(pattern)
            try:
                event = next(iterator)
                event_queue.append((0.0, event))
                iterator_queue.put((event.delta, index, iterator))
            except StopIteration:
                continue
        while iterator_queue.qsize() or len(event_queue):
            if len(event_queue) == 1:
                _, event = event_queue.popleft()
                should_stop = yield event
            elif len(event_queue) > 1:
                offset_one, event_one = event_queue.popleft()
                offset_two, event_two = event_queue.popleft()
                event_queue.appendleft((offset_two, event_two))
                should_stop = yield new(event_one, delta=offset_two - offset_one)
            if iterator_queue.qsize():
                offset, index, iterator = iterator_queue.get()
                try:
                    event = iterator.send(should_stop)
                    event_queue.append((offset, event))
                    iterator_queue.put((offset + event.delta, index, iterator))
                except StopIteration:
                    pass

    ### PUBLIC PROPERTIES ###

    @property
    def is_infinite(self):
        return any(pattern.is_infinite for pattern in self._patterns)
