from queue import PriorityQueue, Empty
from threading import RLock

from .events import Event


class RealtimePatternPlayer:
    def __init__(self, pattern, provider, clock):
        self.pattern = pattern
        self.provider = provider
        self.clock = clock

        # do we need a lock?

        self.lock = RLock()
        self.queue = PriorityQueue()
        self.is_running = False
        self.is_starting = False
        self.is_stopping = False

        self.proxies_by_uuid = {}
        self.notes_by_uuid = {}

    def _clock_callback(self, context, *args, **kwargs):
        # pull from queue
        # consume from iterator if event is none
        # while queue is non-empty
        #    pull from queue events <= desired offset
        #    perform through provider
        with self.lock:
                try:
                    offset, priority, index, event = self.queue.get()
                except Empty:
                    # shutdown
                    return
                if offset == float("-inf"):
                    offset = context.desired_moment.offset
                if not isinstance(event, Event):
                    try:
                        index, event = self.iterator.send(self.is_stopping)
                        for offset, priority, expanded_event in event.expand(
                            context.desired_moment.offset
                        ):
                            self.queue.put((offset, priority, index, expanded_event))
                        self.queue.put((offset + event.delta, 0, index, None))
                    except StopIteration:
                        pass

    def _peek(self):
        try:
            offset, *args = self.queue.get()
            self.queue.put((offset, *args))
            return offset
        except Empty:
            return None

    def play(self, quantization: str = None):
        with self.lock:
            if self.is_running:
                return
        with self.lock:
            self.iterator = enumerate(iter(self.pattern))
            self.queue.put((float("-inf"), 0, 0, None))
        self._clock_event_id = self.clock.cue(
            self._clock_callback,
            event_type=2,
            quantization=quantization,
        )
        if not self.clock.is_running:
            self.clock.start()

    def stop(self, quantization: str = None):
        if not self.is_running:
            return
        # how to handle stopping?
        with self.lock:
            pass
