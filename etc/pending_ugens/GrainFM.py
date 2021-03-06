import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import MultiOutUGen


class GrainFM(MultiOutUGen):
    """

    ::

        >>> grain_fm = supriya.ugens.GrainFM.ar(
        ...     carfrequency=440,
        ...     channel_count=1,
        ...     duration=1,
        ...     envbufnum=-1,
        ...     index=1,
        ...     max_grains=512,
        ...     modfrequency=200,
        ...     pan=0,
        ...     trigger=0,
        ...     )
        >>> grain_fm
        GrainFM.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'channel_count',
        'trigger',
        'duration',
        'carfrequency',
        'modfrequency',
        'index',
        'pan',
        'envbufnum',
        'max_grains',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        carfrequency=440,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        index=1,
        max_grains=512,
        modfrequency=200,
        pan=0,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            carfrequency=carfrequency,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            index=index,
            max_grains=max_grains,
            modfrequency=modfrequency,
            pan=pan,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        carfrequency=440,
        channel_count=1,
        duration=1,
        envbufnum=-1,
        index=1,
        max_grains=512,
        modfrequency=200,
        pan=0,
        trigger=0,
        ):
        """
        Constructs an audio-rate GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm
            GrainFM.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            carfrequency=carfrequency,
            channel_count=channel_count,
            duration=duration,
            envbufnum=envbufnum,
            index=index,
            max_grains=max_grains,
            modfrequency=modfrequency,
            pan=pan,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def carfrequency(self):
        """
        Gets `carfrequency` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.carfrequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('carfrequency')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def duration(self):
        """
        Gets `duration` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.duration
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def envbufnum(self):
        """
        Gets `envbufnum` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.envbufnum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('envbufnum')
        return self._inputs[index]

    @property
    def index(self):
        """
        Gets `index` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.index
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def max_grains(self):
        """
        Gets `max_grains` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.max_grains
            512.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_grains')
        return self._inputs[index]

    @property
    def modfrequency(self):
        """
        Gets `modfrequency` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.modfrequency
            200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('modfrequency')
        return self._inputs[index]

    @property
    def pan(self):
        """
        Gets `pan` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.pan
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('pan')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of GrainFM.

        ::

            >>> grain_fm = supriya.ugens.GrainFM.ar(
            ...     carfrequency=440,
            ...     channel_count=1,
            ...     duration=1,
            ...     envbufnum=-1,
            ...     index=1,
            ...     max_grains=512,
            ...     modfrequency=200,
            ...     pan=0,
            ...     trigger=0,
            ...     )
            >>> grain_fm.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
