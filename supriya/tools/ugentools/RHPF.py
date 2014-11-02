# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class RHPF(Filter):
    r'''Resonant highpass filter unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.RLPF.ar(source=source)
        RLPF.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_q',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        rate=None,
        reciprocal_of_q=1.0,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        r'''Creates an audio-rate resonant highpass filter.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.RLPF.ar(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            RLPF.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        reciprocal_of_q=1.0,
        source=None,
        ):
        r'''Creates a control-rate resonant highpass filter.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.RLPF.kr(
            ...     frequency=440,
            ...     reciprocal_of_q=1.0,
            ...     source=source,
            ...     )
            RLPF.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of RHPF.

        ::

            >>> frequency = None
            >>> rhpf = ugentools.RHPF.ar(
            ...     frequency=frequency,
            ...     )
            >>> rhpf.frequency

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        r'''Gets `reciprocal_of_q` input of RHPF.

        ::

            >>> reciprocal_of_q = None
            >>> rhpf = ugentools.RHPF.ar(
            ...     reciprocal_of_q=reciprocal_of_q,
            ...     )
            >>> rhpf.reciprocal_of_q

        Returns input.
        '''
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of RHPF.

        ::

            >>> source = None
            >>> rhpf = ugentools.RHPF.ar(
            ...     source=source,
            ...     )
            >>> rhpf.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]