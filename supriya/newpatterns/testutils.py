from uuid import UUID

from uqbar.objects import get_repr, get_vars

from .events import CompositeEvent, Event


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


def sanitize(exprs):
    cache = {}
    sanitized = []
    for expr in exprs:
        if isinstance(expr, CompositeEvent):
            sanitized.append(
                CompositeEvent(
                    events=[
                        sanitize_event(child_event, cache)
                        for child_event in expr.events
                    ],
                    delta=expr.delta,
                )
            )
        elif isinstance(expr, Event):
            sanitized.append(sanitize_event(expr, cache))
        else:
            sanitized.append(expr)
    return sanitized


def run_pattern_test(pattern, expected, is_infinite, stop_at):
    assert pattern.is_infinite == is_infinite
    iterator = iter(pattern)
    actual = []
    ceased = True
    for iteration in range(1000):
        try:
            if stop_at == iteration:
                expr = iterator.send(True)
            else:
                expr = next(iterator)
            actual.append(expr)
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
