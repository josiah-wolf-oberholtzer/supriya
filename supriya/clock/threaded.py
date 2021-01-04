import logging
import queue
import threading
from typing import Optional, Tuple

from .bases import BaseTempoClock
from .ephemera import EventType, Moment, TimeUnit

logger = logging.getLogger("supriya.clock")


class TempoClock(BaseTempoClock):

    ### CLASS VARIABLES ###

    _default_clock = None

    ### INITIALIZER ###

    def __init__(self):
        BaseTempoClock.__init__(self)
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command):
        super()._enqueue_command(command)
        self._event.set()

    def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running:
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                return
            try:
                current_moment = self._wait_for_moment()
            except queue.Empty:
                continue
            if current_moment is None:
                return
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
            if not offline:
                self._event.wait(timeout=self._slop)
        logger.debug(f"[{self.name}] Terminating")

    def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self.get_current_time()
        next_time = self._event_queue.peek().seconds
        logger.debug(
            f"[{self.name}] ... Waiting for next moment at {next_time} from {current_time}"
        )
        while current_time < next_time:
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return None
            self._process_command_deque()
            next_time = self._event_queue.peek().seconds
            current_time = self.get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        while not self._event_queue.qsize():
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return False
            self._process_command_deque()
            self._event.clear()
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id) -> Optional[Tuple]:
        logger.debug(f"[{self.name}] Canceling {event_id}")
        event_id = self._cancel(event_id)
        self._event.set()
        return event_id

    def change(
        self,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> Optional[int]:
        return self._change(
            beats_per_minute=beats_per_minute, time_signature=time_signature,
        )

    def cue(
        self,
        procedure,
        *,
        args=None,
        event_type: EventType = EventType.SCHEDULE,
        kwargs=None,
        quantization: str = None,
    ) -> int:
        return self._cue(
            procedure,
            args=args,
            event_type=event_type,
            kwargs=kwargs,
            quantization=quantization,
        )

    def cue_change(
        self,
        *,
        beats_per_minute: Optional[float] = None,
        quantization: str = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ) -> int:
        return self._cue_change(
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
            quantization=quantization,
        )

    @classmethod
    def default(cls):
        if cls._default_clock is None:
            cls._default_clock = cls()
        return cls._default_clock

    def reschedule(
        self, event_id, *, schedule_at=0.0, time_unit=TimeUnit.BEATS
    ) -> Optional[int]:
        if (event_or_command := self.cancel(event_id)) is None:
            return None
        command = self._reschedule(
            event_or_command, schedule_at=schedule_at, time_unit=time_unit,
        )
        self._enqueue_command(command)
        return event_id

    def schedule(
        self,
        procedure,
        *,
        event_type: EventType = EventType.SCHEDULE,
        schedule_at: float = 0.0,
        time_unit: TimeUnit = TimeUnit.BEATS,
        args=None,
        kwargs=None,
    ) -> int:
        return self._schedule(
            procedure,
            event_type=event_type,
            schedule_at=schedule_at,
            time_unit=time_unit,
            args=args,
            kwargs=kwargs,
        )

    def schedule_change(
        self,
        *,
        beats_per_minute: Optional[float] = None,
        schedule_at: float = 0.0,
        time_signature: Optional[Tuple[int, int]] = None,
        time_unit: TimeUnit = TimeUnit.BEATS,
    ) -> int:
        return self._schedule_change(
            beats_per_minute=beats_per_minute,
            schedule_at=schedule_at,
            time_signature=time_signature,
            time_unit=time_unit,
        )

    def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ):
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._thread = threading.Thread(target=self._run, args=(self,), daemon=True)
        self._thread.start()

    def stop(self):
        if self._stop():
            self._event.set()
            self._thread.join()
