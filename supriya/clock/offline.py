import logging
import queue
from typing import Optional, Tuple

from .bases import BaseTempoClock
from .ephemera import (
    CallbackCommand,
    ChangeCommand,
    EventType,
    Moment,
    TimeUnit,
)

logger = logging.getLogger("supriya.clock")


class OfflineTempoClock(BaseTempoClock):

    ### SCHEDULING METHODS ###

    def _cancel(self, event_id) -> Optional[Tuple]:
        event = self._events_by_id.pop(event_id, None)
        if event is not None and not isinstance(
            event, (CallbackCommand, ChangeCommand)
        ):
            self._event_queue.remove(event)
            if event.offset is not None:
                self._offset_relative_event_ids.remove(event.event_id)
                if event.measure is not None:
                    self._measure_relative_event_ids.remove(event.event_id)
        return event

    def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
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
        logger.debug(f"[{self.name}] Terminating")

    def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        while not self._event_queue.qsize():
            if not self._is_running:
                return False
            self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id) -> Optional[Tuple]:
        logger.debug(f"[{self.name}] Canceling {event_id}")
        event_id = self._cancel(event_id)
        return event_id

    def get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds

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
        self._run()

    def stop(self):
        self._stop()
