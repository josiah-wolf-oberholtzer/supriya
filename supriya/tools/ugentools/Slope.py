# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Slope(Filter):
    r"""
    Calculates slope of signal.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> slope = ugentools.Slope.ar(
        ...     source=source,
        ...     )
        >>> slope
        Slope.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r"""
        Constructs an audio-rate Slope.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> slope = ugentools.Slope.ar(
            ...     source=source,
            ...     )
            >>> slope
            Slope.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r"""
        Constructs a control-rate Slope.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> slope = ugentools.Slope.kr(
            ...     source=source,
            ...     )
            >>> slope
            Slope.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r"""
        Gets `source` input of Slope.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> slope = ugentools.Slope.ar(
            ...     source=source,
            ...     )
            >>> slope.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
