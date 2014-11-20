# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class FFT(PV_ChainUGen):
    r'''A fast Fourier transform.

    ::

        >>> buffer_id = ugentools.LocalBuf(2048)
        >>> source = ugentools.SoundIn.ar(bus=0)
        >>> fft = ugentools.FFT(
        ...     active=1,
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     source=source,
        ...     window_size=0,
        ...     window_type=0,
        ...     )
        >>> fft
        FFT.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'hop',
        'window_type',
        'active',
        'window_size',
        )

    _valid_calculation_rates = (
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        source=None,
        calculation_rate=None,
        active=1,
        hop=0.5,
        window_size=0,
        window_type=0,
        ):
        from supriya.tools import synthdeftools
        if calculation_rate is None:
            calculation_rate = synthdeftools.CalculationRate.CONTROL
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        active=1,
        buffer_id=None,
        hop=0.5,
        source=None,
        window_size=0,
        window_type=0,
        ):
        r'''Constructs a FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT.new(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft
            FFT.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def active(self):
        r'''Gets `active` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.active
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('active')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.buffer_id
            OutputProxy(
                source=LocalBuf(
                    frame_count=2048.0,
                    calculation_rate=<CalculationRate.SCALAR: 0>,
                    channel_count=1.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def hop(self):
        r'''Gets `hop` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.hop
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hop')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.source
            OutputProxy(
                source=In(
                    bus=OutputProxy(
                        source=NumOutputBuses(
                            calculation_rate=<CalculationRate.SCALAR: 0>
                            ),
                        output_index=0
                        ),
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def window_size(self):
        r'''Gets `window_size` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_size
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]

    @property
    def window_type(self):
        r'''Gets `window_type` input of FFT.

        ::

            >>> buffer_id = ugentools.LocalBuf(2048)
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> fft = ugentools.FFT(
            ...     active=1,
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     source=source,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_type
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('window_type')
        return self._inputs[index]