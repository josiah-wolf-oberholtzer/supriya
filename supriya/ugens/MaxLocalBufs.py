import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class MaxLocalBufs(UGen):
    """
    Sets the maximum number of local buffers in a synth.

    Used internally by LocalBuf.

    ::

        >>> max_local_bufs = supriya.ugens.MaxLocalBufs(1)
        >>> max_local_bufs
        MaxLocalBufs.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Buffer UGens"

    _ordered_input_names = collections.OrderedDict([("maximum", 0)])

    _valid_calculation_rates = (CalculationRate.SCALAR,)

    ### INITIALIZER ###

    def __init__(self, maximum=0):
        import supriya.synthdefs

        maximum = float(maximum)
        calculation_rate = supriya.CalculationRate.SCALAR
        UGen.__init__(self, calculation_rate=calculation_rate, maximum=maximum)

    ### PUBLIC METHODS ###

    def increment(self):
        """
        Increments maximum local buffer count.

        ::

            >>> max_local_bufs = supriya.ugens.MaxLocalBufs(1)
            >>> max_local_bufs.maximum
            1.0

        ::

            >>> max_local_bufs.increment()
            >>> max_local_bufs.maximum
            2.0

        Returns none.
        """
        self._inputs[0] += 1
