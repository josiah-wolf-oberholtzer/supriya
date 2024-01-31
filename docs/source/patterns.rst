Patterns
========

- what is a pattern
- quick example
- legacy of sc's pattern library
- equivalences

Supriya provides a library of composable "pattern" classes for generating
sequences of musical events.

Supriya's pattern library is heavily inspired by SuperCollider's own pattern
classes, and re-implements a small subset of those classes in Python.

Sequences
---------

- sequence pattern

Iterating
`````````

- iterations=1
- iterations=2
- iterations=None

Math
----

- unary op pattern
- binary op pattern

Noise
-----

Randomizing
```````````

- RandomPattern

Choosing
````````

- ChoicePattern

Shuffling
`````````

- ShufflePattern

Events
------

- EventPattern
- MonoEventPattern
- Event beastiary

Structure
---------

- GroupPattern
- FxPattern
- ParallelPattern
- BusPattern

Playing
-------

- patterns are stateless
- contexts: realtime and non-realtime
- starting and stopping
- timing: clocks, quantization, at, until
- target node, target bus
- event callbacks
