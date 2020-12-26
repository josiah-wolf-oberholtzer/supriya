from uuid import UUID

from uqbar.objects import get_repr, get_vars

from .events import CompositeEvent


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


def run_event_pattern_test(pattern, expected, is_infinite, stop_at):
    assert pattern.is_infinite == is_infinite
    iterator = iter(pattern)
    actual = []
    ceased = True
    for iteration in range(1000):
        try:
            if stop_at == iteration:
                event = iterator.send(True)
            else:
                event = next(iterator)
            actual.append(event)
        except StopIteration:
            break
    else:
        ceased = False
    if is_infinite:
        assert not ceased
        sanitized_actual = sanitize(actual[: len(expected)])
    else:
        sanitized_actual = sanitize(actual)
    assert sanitized_actual == expected, sanitized_actual
