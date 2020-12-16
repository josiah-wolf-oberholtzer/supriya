"""
The core pattern classes.
"""
import abc
import inspect
import itertools
import operator
import random
from collections.abc import Sequence
from typing import Dict, Iterator


class Pattern(metaclass=abc.ABCMeta):

    ### CLASSMETHODS ###

    _rngs: Dict[int, Iterator[float]] = {}

    ### SPECIAL METHODS ###

    def __abs__(self):
        return UnaryOpPattern(self)

    def __add__(self, expr):
        return BinaryOpPattern(self, "+", expr)

    def __div__(self, expr):
        return BinaryOpPattern(self, "/", expr)

    def __invert__(self):
        return UnaryOpPattern(self, "~")

    def __iter__(self):
        should_stop = False
        iterator = self._iterate()
        try:
            initial_expr = next(iterator)
        except StopIteration:
            return
        should_stop = yield initial_expr
        while True:
            try:
                expr = iterator.send(should_stop)
                should_stop = yield expr
            except StopIteration:
                break

    def __mod__(self, expr):
        return BinaryOpPattern(self, "%", expr)

    def __mul__(self, expr):
        return BinaryOpPattern(self, "*", expr)

    def __neg__(self):
        return UnaryOpPattern(self, "-")

    def __pos__(self):
        return UnaryOpPattern(self, "+")

    def __pow__(self, expr):
        return BinaryOpPattern(self, "**", expr)

    def __radd__(self, expr):
        return BinaryOpPattern(expr, "+", self)

    def __rdiv__(self, expr):
        return BinaryOpPattern(expr, "/", self)

    def __rmod__(self, expr):
        return BinaryOpPattern(expr, "%", self)

    def __rmul__(self, expr):
        return BinaryOpPattern(expr, "*", self)

    def __rpow__(self, expr):
        return BinaryOpPattern(expr, "**", self)

    def __rsub__(self, expr):
        return BinaryOpPattern(expr, "-", self)

    def __sub__(self, expr):
        return BinaryOpPattern(self, "-", expr)

    ### PRIVATE METHODS ###

    def _apply_recursive(self, procedure, *exprs):
        if all(not isinstance(x, Sequence) for x in exprs):
            return procedure(*exprs)
        coerced_exprs = [
            expr if isinstance(expr, Sequence) else [expr] for expr in exprs
        ]
        max_length = max(len(expr) for expr in coerced_exprs)
        for i, expr in enumerate(coerced_exprs):
            if len(expr) < max_length:
                cycle = itertools.cycle(expr)
                coerced_exprs[i] = [next(cycle) for _ in range(max_length)]
        return [
            self._apply_recursive(procedure, *items) for items in zip(*coerced_exprs)
        ]

    def _freeze_recursive(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, Sequence) and not isinstance(value, Pattern):
            return tuple(self._freeze_recursive(_) for _ in value)
        return value

    def _get_arity(self, value):
        if isinstance(value, Pattern):
            return value.arity
        elif isinstance(value, Sequence):
            return len(value)
        return 1

    def _get_rng(self):
        identifier = None
        try:
            # Walk frames to find an enclosing SeedPattern._iterate()
            frame = inspect.currentframe()
            while frame is not None:
                if (
                    isinstance(frame.f_locals.get("self"), SeedPattern)
                    and frame.f_code.co_name == "_iterate"
                ):
                    identifier = id(frame)
                    break
                frame = frame.f_back
        finally:
            del frame
        if identifier in self._rngs:
            return self._rngs[identifier]
        return self._get_stdlib_rng()

    def _get_seeded_rng(self, seed: int = 1) -> Iterator[float]:
        while True:
            seed = (seed * 1_103_515_245 + 12345) & 0x7FFFFFFF
            yield float(seed) / 0x7FFFFFFF

    def _get_stdlib_rng(self) -> Iterator[float]:
        while True:
            yield random.random()

    @abc.abstractmethod
    def _iterate(self):
        raise NotImplementedError

    def _loop(self, iterations=None):
        if iterations is None:
            while True:
                yield True
        else:
            for _ in range(iterations):
                yield True

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arity(self):
        raise NotImplementedError

    @abc.abstractproperty
    def is_infinite(self):
        raise NotImplementedError


class BinaryOpPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, expr_one, operator, expr_two):
        self._expr_one = self._freeze_recursive(expr_one)
        self._expr_two = self._freeze_recursive(expr_two)
        self._operator = operator

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        expr_one = self.expr_one
        if not isinstance(expr_one, Pattern):
            expr_one = SequencePattern([expr_one], None)
        expr_one = iter(expr_one)
        expr_two = self.expr_two
        if not isinstance(expr_two, Pattern):
            expr_two = SequencePattern([expr_two], None)
        expr_two = iter(expr_two)
        operator = self._string_to_operator()
        for item_one, item_two in zip(expr_one, expr_two):
            yield self._apply_recursive(operator, item_one, item_two)

    def _string_to_operator(self):
        operators = {
            "%": operator.__mod__,
            "*": operator.__mul__,
            "**": operator.__pow__,
            "+": operator.__add__,
            "-": operator.__sub__,
            "/": operator.__truediv__,
            "//": operator.__floordiv__,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self.__get_arity(x) for x in (self._expr_one, self._expr_two))

    @property
    def expr_one(self):
        return self._expr_one

    @property
    def expr_two(self):
        return self._expr_two

    @property
    def is_infinite(self):
        return (
            isinstance(self.expr_one, Pattern)
            and isinstance(self.expr_two, Pattern)
            and self.expr_one.is_infinite
            and self.expr_two.is_infinite
        )

    @property
    def operator(self):
        return self._operator


class UnaryOpPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, expr, operator):
        self._expr = expr
        self._operator = operator

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        expr = self.expr
        if not isinstance(expr, Pattern):
            expr = SequencePattern([expr], None)
        expr = iter(expr)
        operator = self._string_to_operator()
        for item in expr:
            yield self._apply_recursive(operator, item)

    def _string_to_operator(self):
        operators = {
            "~": operator.invert,
            "-": operator.__neg__,
            "+": operator.__pos__,
            "abs": operator.abs,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._get_arity(self.expr)

    @property
    def expr(self):
        return self._expr

    @property
    def is_infinite(self):
        return isinstance(self.expr, Pattern) and self.expr.is_infinite

    @property
    def operator(self):
        return self._operator


class SeedPattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, pattern, seed=0):
        if not isinstance(pattern, Pattern):
            raise ValueError(f"Must be pattern: {pattern!r}")
        self._pattern = pattern
        self._seed = int(seed)

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        try:
            identifier = id(inspect.currentframe())
            rng = self._get_seeded_rng(seed=self.seed)
            self._rngs[identifier] = rng
            yield from self._pattern
        finally:
            del self._rngs[identifier]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern

    @property
    def seed(self):
        return self._seed


class SequencePattern(Pattern):

    ### INITIALIZER ###

    def __init__(self, sequence, iterations=1):
        if not isinstance(sequence, Sequence):
            raise ValueError(f"Must be sequence: {sequence!r}")
        if iterations is not None:
            iterations = int(iterations)
            if iterations < 1:
                raise ValueError("Iterations must be null or greater than 0")
        self._sequence = self._freeze_recursive(sequence)
        self._iterations = iterations

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        should_stop = False
        for _ in self._loop(self._iterations):
            for x in self._sequence:
                if not isinstance(x, Pattern):
                    should_stop = yield x
                else:
                    iterator = iter(x)
                    try:
                        y = next(iterator)
                        should_stop = yield y
                        while True:
                            y = iterator.send(should_stop)
                            should_stop = yield y
                    except StopIteration:
                        pass
                if should_stop:
                    return

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(x) for x in self.sequence)

    @property
    def is_infinite(self):
        if self.iterations is None:
            return True
        for x in self.sequence:
            if isinstance(x, Pattern) and x.is_infinite:
                return True
        return False
