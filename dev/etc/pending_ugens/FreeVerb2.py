import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import MultiOutUGen


class FreeVerb2(MultiOutUGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
        ...     damping=0.5,
        ...     in_2=in_2,
        ...     mix=0.33,
        ...     room=0.5,
        ...     source=source,
        ...     )
        >>> free_verb_2
        FreeVerb2.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'source',
        'in_2',
        'mix',
        'room',
        'damping',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        """
        Constructs an audio-rate FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2
            FreeVerb2.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        """
        Gets `damping` input of FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.damping
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def in_2(self):
        """
        Gets `in_2` input of FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.in_2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_2')
        return self._inputs[index]

    @property
    def mix(self):
        """
        Gets `mix` input of FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.mix
            0.33

        Returns ugen input.
        """
        index = self._ordered_input_names.index('mix')
        return self._inputs[index]

    @property
    def room(self):
        """
        Gets `room` input of FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.room
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('room')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of FreeVerb2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb_2 = supriya.ugens.FreeVerb2.ar(
            ...     damping=0.5,
            ...     in_2=in_2,
            ...     mix=0.33,
            ...     room=0.5,
            ...     source=source,
            ...     )
            >>> free_verb_2.source
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
