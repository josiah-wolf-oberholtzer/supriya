import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class IEnvGen(UGen):
    """

    ::

        >>> ienv_gen = supriya.ugens.IEnvGen.ar(
        ...     envelope=envelope,
        ...     index=index,
        ...     )
        >>> ienv_gen
        IEnvGen.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'envelope',
        'index',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        envelope=None,
        index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        envelope=None,
        index=None,
        ):
        """
        Constructs an audio-rate IEnvGen.

        ::

            >>> ienv_gen = supriya.ugens.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen
            IEnvGen.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def convertEnv(): ...

    @classmethod
    def kr(
        cls,
        envelope=None,
        index=None,
        ):
        """
        Constructs a control-rate IEnvGen.

        ::

            >>> ienv_gen = supriya.ugens.IEnvGen.kr(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen
            IEnvGen.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def envelope(self):
        """
        Gets `envelope` input of IEnvGen.

        ::

            >>> ienv_gen = supriya.ugens.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen.envelope

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envelope')
        return self._inputs[index]

    @property
    def index(self):
        """
        Gets `index` input of IEnvGen.

        ::

            >>> ienv_gen = supriya.ugens.IEnvGen.ar(
            ...     envelope=envelope,
            ...     index=index,
            ...     )
            >>> ienv_gen.index

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index')
        return self._inputs[index]
