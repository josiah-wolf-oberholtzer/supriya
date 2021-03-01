from queue import Empty, PriorityQueue
from threading import RLock

from .events import Event


class RealtimePatternPlayer:
    def __init__(self, pattern, provider, clock):
        self._pattern = pattern
        self._provider = provider
        self._clock = clock
        self._lock = RLock()
        self._queue = PriorityQueue()
        self._is_running = False
        self._is_stopping = False
        self._proxies_by_uuid = {}
        self._notes_by_uuid = {}

    def _clock_callback(self, context, *args, **kwargs):
        with self._lock:
            current_offset = None
            events = []
            while True:
                try:
                    offset, priority, index, event = self._queue.get(block=False)
                except Empty:
                    self._perform_events(current_offset, events)
                    self._is_running = False
                    return None
                except Exception:
                    return
                if offset == float("-inf"):
                    offset = context.desired_moment.offset
                if (delta := offset - context.desired_moment.offset) :
                    self._queue.put((offset, priority, index, event))
                    self._perform_events(current_offset, events)
                    return delta
                if not isinstance(event, Event):
                    if self._consume_iterator(offset):
                        return
                elif offset != current_offset:
                    self._perform_events(current_offset, events)
                    current_offset = offset
                    events = [(event, priority)]
                else:
                    events.append((event, priority))

    def _consume_iterator(self, current_offset):
        try:
            try:
                index, consumed_event = self._iterator.send(self._is_stopping)
            except TypeError:
                if self._is_stopping:
                    return True
                index, consumed_event = next(self._iterator)
            for (expanded_offset, priority, expanded_event,) in consumed_event.expand(
                current_offset
            ):
                self._queue.put((expanded_offset, priority, index, expanded_event))
            self._queue.put((current_offset + consumed_event.delta, 0, index, None))
        except StopIteration:
            pass
        return False

    def _stop_callback(self, context, *args, **kwargs):
        with self._lock:
            # Do we need to rebuild the queue?
            # Do we need to free all playing notes?
            # How do we handle when there are already stop events in the queue?
            self._is_stopping = True

    def _enumerate(self, iterator):
        index = 0
        should_stop = False
        while True:
            try:
                should_stop = yield (index, iterator.send(should_stop)) or should_stop
            except TypeError:
                should_stop = yield (index, next(iterator))
            except StopIteration:
                return
            index += 1

    def _perform_events(self, current_offset, events):
        if not events:
            return
        with self._provider.at(current_offset):
            for event, priority in events:
                event.perform(
                    self._provider,
                    self._proxies_by_uuid,
                    current_offset=current_offset,
                    notes_mapping=self._notes_by_uuid,
                    priority=priority,
                )

    def play(self, quantization: str = None):
        with self._lock:
            if self._is_running:
                return
            self._iterator = self._enumerate(iter(self._pattern))
            self._queue.put((float("-inf"), 0, 0, None))
            self._is_running = True
            self._is_stopping = False
        self._clock_event_id = self._clock.cue(
            self._clock_callback, event_type=3, quantization=quantization,
        )
        if not self._clock.is_running:
            self._clock.start()

    def stop(self, quantization: str = None):
        with self._lock:
            if not self._is_running or self._is_stopping:
                return
            self._clock.cue(
                self._stop_callback, event_type=2, quantization=quantization,
            )