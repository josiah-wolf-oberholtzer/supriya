import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class DynKlang(UGen):
    """

    ::

        >>> dyn_klang = supriya.ugens.DynKlang.ar(
        ...     freqoffset=0,
        ...     freqscale=1,
        ...     specifications_array_ref=specifications_array_ref,
        ...     )
        >>> dyn_klang
        DynKlang.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'specifications_array_ref',
        'freqscale',
        'freqoffset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        """
        Constructs an audio-rate DynKlang.

        ::

            >>> dyn_klang = supriya.ugens.DynKlang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klang
            DynKlang.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        """
        Constructs a control-rate DynKlang.

        ::

            >>> dyn_klang = supriya.ugens.DynKlang.kr(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klang
            DynKlang.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def freqoffset(self):
        """
        Gets `freqoffset` input of DynKlang.

        ::

            >>> dyn_klang = supriya.ugens.DynKlang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klang.freqoffset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqoffset')
        return self._inputs[index]

    @property
    def freqscale(self):
        """
        Gets `freqscale` input of DynKlang.

        ::

            >>> dyn_klang = supriya.ugens.DynKlang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klang.freqscale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqscale')
        return self._inputs[index]

    @property
    def specifications_array_ref(self):
        """
        Gets `specifications_array_ref` input of DynKlang.

        ::

            >>> dyn_klang = supriya.ugens.DynKlang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> dyn_klang.specifications_array_ref

        Returns ugen input.
        """
        index = self._ordered_input_names.index('specifications_array_ref')
        return self._inputs[index]
