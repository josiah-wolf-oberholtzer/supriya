Non-realtime Scores
===================

Lifecycle
---------

::

    >>> score = supriya.Score()

::

    >>> with score.at(0):
    ...     with score.add_synthdefs(supriya.default):
    ...         synth = score.add_synth(supriya.default)
    ...
    >>> with score.at(2):
    ...     synth.set(frequency=550)
    ...
    >>> with score.at(4):
    ...     synth.free()
    ...

::

    >>> with score.at(5):
    ...     score.do_nothing()
    ...


::

    >>> asyncio.run(score.render())

Options
```````

- Options
- Input / output bus counts

Rendering
`````````

- Specifying output path
- Render directory
- Specifying input path
- Suppressing output

Inspection
----------

::

    >>> for request_bundle in score.iterate_request_bundles():
    ...     request_bundle
    ...

::

    >>> for osc_bundle in score.iterate_osc_bundles():
    ...     osc_bundle
    ...

Interaction
-----------

::

    >>> score.setup_system_synthdefs()
