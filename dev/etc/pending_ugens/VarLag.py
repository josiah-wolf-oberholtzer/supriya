import collections
from supriya.enums import CalculationRate
from supriya.ugens.Filter import Filter


class VarLag(Filter):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> var_lag = supriya.ugens.VarLag.ar(
        ...     curvature=0,
        ...     source=source,
        ...     start=start,
        ...     time=0.1,
        ...     warp=5,
        ...     )
        >>> var_lag
        VarLag.ar()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = collections.OrderedDict(
        'source',
        'time',
        'curvature',
        'warp',
        'start',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        """
        Constructs an audio-rate VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag
            VarLag.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        curvature=0,
        source=None,
        start=None,
        time=0.1,
        warp=5,
        ):
        """
        Constructs a control-rate VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.kr(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag
            VarLag.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def new1(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def curvature(self):
        """
        Gets `curvature` input of VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.curvature
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('curvature')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.source
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

    @property
    def start(self):
        """
        Gets `start` input of VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.start

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def time(self):
        """
        Gets `time` input of VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.time
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('time')
        return self._inputs[index]

    @property
    def warp(self):
        """
        Gets `warp` input of VarLag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> var_lag = supriya.ugens.VarLag.ar(
            ...     curvature=0,
            ...     source=source,
            ...     start=start,
            ...     time=0.1,
            ...     warp=5,
            ...     )
            >>> var_lag.warp
            5.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('warp')
        return self._inputs[index]
