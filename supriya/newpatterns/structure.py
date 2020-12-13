from .patterns import Pattern


class BusPattern(Pattern):
    def __init__(self, pattern):
        pass


class FxPattern(Pattern):
    def __init__(self, pattern):
        pass


class GroupPattern(Pattern):
    def __init__(self, pattern):
        pass


class ParallelPattern(Pattern):
    def __init__(self, patterns, *, with_groups=False):
        pass


class StructurePattern(Pattern):
    def __init__(
        self,
        patterns,
        *,
        with_buses=False,
        with_groups=False,
        with_synthdef=None,
        **kwargs,
    ):
        pass
