import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import MultiOutUGen


class XFadeRotate(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> xfade_rotate = supriya.ugens.XFadeRotate.ar(
        ...     n=0,
        ...     source=source,
        ...     )
        >>> xfade_rotate
        XFadeRotate.ar()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = collections.OrderedDict(
        'n',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        n=0,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        n=0,
        source=None,
        ):
        """
        Constructs an audio-rate XFadeRotate.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> xfade_rotate = supriya.ugens.XFadeRotate.ar(
            ...     n=0,
            ...     source=source,
            ...     )
            >>> xfade_rotate
            XFadeRotate.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        n=0,
        source=None,
        ):
        """
        Constructs a control-rate XFadeRotate.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> xfade_rotate = supriya.ugens.XFadeRotate.kr(
            ...     n=0,
            ...     source=source,
            ...     )
            >>> xfade_rotate
            XFadeRotate.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        """
        Gets `n` input of XFadeRotate.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> xfade_rotate = supriya.ugens.XFadeRotate.ar(
            ...     n=0,
            ...     source=source,
            ...     )
            >>> xfade_rotate.n
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('n')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of XFadeRotate.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> xfade_rotate = supriya.ugens.XFadeRotate.ar(
            ...     n=0,
            ...     source=source,
            ...     )
            >>> xfade_rotate.source
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
