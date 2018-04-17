from supriya.ugens.PV_ChainUGen import PV_ChainUGen


class PV_RandComb(PV_ChainUGen):
    """
    Passes random bins.

    ::

        >>> pv_chain = supriya.ugens.FFT(
        ...     source=supriya.ugens.WhiteNoise.ar(),
        ...     )
        >>> pv_rand_comb = supriya.ugens.PV_RandComb(
        ...     pv_chain=pv_chain,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_comb
        PV_RandComb.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'pv_chain',
        'wipe',
        'trigger',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pv_chain=None,
        trigger=0,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            pv_chain=pv_chain,
            trigger=trigger,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        pv_chain=None,
        trigger=0,
        wipe=0,
        ):
        """
        Constructs a PV_RandComb.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_rand_comb = supriya.ugens.PV_RandComb.new(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb
            PV_RandComb.kr()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            pv_chain=pv_chain,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def pv_chain(self):
        """
        Gets `pv_chain` input of PV_RandComb.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_rand_comb = supriya.ugens.PV_RandComb(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.pv_chain
            FFT.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pv_chain')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of PV_RandComb.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_rand_comb = supriya.ugens.PV_RandComb(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def wipe(self):
        """
        Gets `wipe` input of PV_RandComb.

        ::

            >>> pv_chain = supriya.ugens.FFT(
            ...     source=supriya.ugens.WhiteNoise.ar(),
            ...     )
            >>> pv_rand_comb = supriya.ugens.PV_RandComb(
            ...     pv_chain=pv_chain,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_comb.wipe
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]