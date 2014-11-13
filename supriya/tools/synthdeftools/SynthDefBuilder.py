# -*- encoding: utf-8 -*-
import collections
from abjad.tools.topleveltools import new
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefBuilder(SupriyaObject):
    r'''A SynthDef builder.

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder()
        >>> builder.add_parameter('frequency', 440)
        >>> builder.add_parameter(
        ...     'trigger', 0, synthdeftools.ParameterRate.TRIGGER,
        ...     )
        >>> sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
        >>> decay = ugentools.Decay.kr(
        ...     decay_time=0.5,
        ...     source=builder['trigger'],
        ...     )
        >>> enveloped_sin = sin_osc * decay
        >>> out = ugentools.Out.ar(bus=0, source=enveloped_sin)
        >>> builder.add_ugen(out)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_parameters',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        **kwargs
        ):
        self._parameters = {}
        for key, value in kwargs.items():
            self.add_parameter(key, value)
        self._ugens = []

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._parameters[item]

    ### PUBLIC METHODS ###

    def add_parameter(self, *args):
        from supriya.tools import synthdeftools
        if 3 < len(args):
            raise ValueError(args)
        if len(args) == 1:
            assert isinstance(args[0], synthdeftools.Parameter)
            name, value, parameter_rate = \
                args[0].name, args[0], args[0].parameter_rate
        elif len(args) == 2:
            name, value = args
            parameter_rate = synthdeftools.ParameterRate.SCALAR
            if not isinstance(value, synthdeftools.Parameter):
                if name.startswith('a_'):
                    parameter_rate = synthdeftools.ParameterRate.AUDIO
                elif name.startswith('i_'):
                    parameter_rate = synthdeftools.ParameterRate.SCALAR
                elif name.startswith('t_'):
                    parameter_rate = synthdeftools.ParameterRate.TRIGGER
                else:
                    parameter_rate = synthdeftools.ParameterRate.CONTROL
        elif len(args) == 3:
            name, value, parameter_rate = args
            parameter_rate = synthdeftools.ParameterRate.from_expr(
                parameter_rate,
                )
        else:
            raise ValueError(args)
        if not isinstance(value, synthdeftools.Parameter):
            parameter = synthdeftools.Parameter(
                name=name,
                parameter_rate=parameter_rate,
                value=value,
                )
        else:
            parameter = new(
                value,
                parameter_rate=parameter_rate,
                name=name,
                )
        self._parameters[name] = parameter

    def poll_ugen(
        self,
        ugen,
        label=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import ugentools
        if trigger is None:
            trigger = ugentools.Impulse.kr(1)
        poll = ugentools.Poll.new(
            source=ugen,
            label=label,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        self.add_ugen(poll)

    def add_ugen(self, ugens):
        from supriya.tools import synthdeftools
        if not isinstance(ugens, collections.Sequence):
            ugens = [ugens]
        prototype = (
            synthdeftools.UGen,
            synthdeftools.OutputProxy,
            synthdeftools.Parameter,
            )
        for ugen in ugens:
            assert isinstance(ugen, prototype), type(ugen)
            if isinstance(ugen, synthdeftools.OutputProxy):
                ugen = ugen.source
            if ugen not in self._ugens:
                self._ugens.append(ugen)

    def build(self, name=None):
        from supriya.tools import synthdeftools
        ugens = list(self._parameters.values()) + list(self._ugens)
        synthdef = synthdeftools.SynthDef(
            ugens,
            name=name,
            )
        return synthdef