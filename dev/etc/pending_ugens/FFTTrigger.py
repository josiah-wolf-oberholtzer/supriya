import collections
from supriya.enums import CalculationRate
from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class FFTTrigger(PV_ChainUGen):
    """

    ::

        >>> ffttrigger = supriya.ugens.FFTTrigger.ar(
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     polar=0,
        ...     )
        >>> ffttrigger
        FFTTrigger.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'buffer_id',
        'hop',
        'polar',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        hop=0.5,
        polar=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            hop=hop,
            polar=polar,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        hop=0.5,
        polar=0,
        ):
        """
        Constructs a FFTTrigger.

        ::

            >>> ffttrigger = supriya.ugens.FFTTrigger.new(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger
            FFTTrigger.new()

        Returns ugen graph.
        """
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            hop=hop,
            polar=polar,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of FFTTrigger.

        ::

            >>> ffttrigger = supriya.ugens.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.buffer_id

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def hop(self):
        """
        Gets `hop` input of FFTTrigger.

        ::

            >>> ffttrigger = supriya.ugens.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.hop
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('hop')
        return self._inputs[index]

    @property
    def polar(self):
        """
        Gets `polar` input of FFTTrigger.

        ::

            >>> ffttrigger = supriya.ugens.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.polar
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('polar')
        return self._inputs[index]
