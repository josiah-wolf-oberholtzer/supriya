from supriya import utils
import supriya.system


class ServerMeters(supriya.system.SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_input_meter_callback',
        '_input_meter_peak_levels',
        '_input_meter_rms_levels',
        '_input_meter_synth',
        '_output_meter_callback',
        '_output_meter_peak_levels',
        '_output_meter_rms_levels',
        '_output_meter_synth',
        '_server',
        )

    ### INITIALIZER ###

    def __init__(self, server):
        self._server = server
        self._input_meter_callback = None
        self._input_meter_peak_levels = None
        self._input_meter_rms_levels = None
        self._input_meter_synth = None
        self._output_meter_callback = None
        self._output_meter_peak_levels = None
        self._output_meter_rms_levels = None
        self._output_meter_synth = None

    ### PUBLIC METHODS ###

    @staticmethod
    def make_meter_synthdef(
        channel_count=1,
        command_name='/reply',
        initial_bus=0,
        ):
        import supriya.synthdefs
        import supriya.ugens
        with supriya.synthdefs.SynthDefBuilder() as builder:
            source = supriya.ugens.In.ar(
                bus=initial_bus,
                channel_count=channel_count,
                )
            supriya.ugens.SendPeakRMS.kr(
                command_name=command_name,
                peak_lag=1,
                reply_rate=20,
                source=source,
                )
        synthdef = builder.build()
        return synthdef

    ### PRIVATE METHODS ###

    def _handle_input_levels(self, message):
        contents = message.contents[2:]
        peak_levels = []
        rms_levels = []
        for peak, rms in utils.group_iterable_by_count(contents, 2):
            peak_levels.append(peak)
            rms_levels.append(rms)
        self._input_meter_peak_levels = tuple(peak_levels)
        self._input_meter_rms_levels = tuple(rms_levels)

    def _handle_output_levels(self, message):
        contents = message.contents[2:]
        peak_levels = []
        rms_levels = []
        for peak, rms in utils.group_iterable_by_count(contents, 2):
            peak_levels.append(peak)
            rms_levels.append(rms)
        self._output_meter_peak_levels = tuple(peak_levels)
        self._output_meter_rms_levels = tuple(rms_levels)
        supriya.system.PubSub.notify(
            'server-meters',
            {
                'input_meter_peak_levels': self._input_meter_peak_levels,
                'input_meter_rms_levels': self._input_meter_rms_levels,
                'output_meter_peak_levels': self._output_meter_peak_levels,
                'output_meter_rms_levels': self._output_meter_rms_levels,
                },
            )

    ### PUBLIC METHODS ###

    @supriya.system.PubSub.subscribe_before('server-quitting')
    def allocate(self):
        import supriya.osc
        import supriya.realtime
        self._input_meter_callback = supriya.osc.OscCallback(
            address_pattern=self.input_meter_command,
            procedure=self._handle_input_levels,
            )
        self._output_meter_callback = supriya.osc.OscCallback(
            address_pattern=self.output_meter_command,
            procedure=self._handle_output_levels,
            )
        self.server.register_osc_callback(self._input_meter_callback)
        self.server.register_osc_callback(self._output_meter_callback)
        input_meter_synthdef = self.input_meter_synthdef
        output_meter_synthdef = self.output_meter_synthdef
        self._input_meter_synth = supriya.realtime.Synth(
            input_meter_synthdef,
            )
        self._output_meter_synth = supriya.realtime.Synth(
            output_meter_synthdef,
            )
        self._input_meter_synth.allocate(
            add_action=supriya.realtime.AddAction.ADD_TO_HEAD,
            node_id_is_permanent=True,
            target_node=self.server.root_node,
            )
        self._output_meter_synth.allocate(
            add_action=supriya.realtime.AddAction.ADD_TO_TAIL,
            node_id_is_permanent=True,
            target_node=self.server.root_node,
            )
        return self

    @supriya.system.PubSub.unsubscribe_after('server-quitting')
    def free(self):
        self.server.unregister_osc_callback(self._input_meter_callback)
        self.server.unregister_osc_callback(self._output_meter_callback)
        self._input_meter_synth.free()
        self._output_meter_synth.free()
        self._input_meter_callback = None
        self._output_meter_callback = None
        self._input_meter_synth = None
        self._output_meter_synth = None

    def notify(self, topic, event):
        if topic == 'server-quitting':
            self.free()

    def to_dict(self):
        input_meter_levels, output_meter_levels = [], []
        for peak, rms in zip(
            self._input_meter_peak_levels,
            self._input_meter_rms_levels,
            ):
            input_meter_levels.append(dict(peak=peak, rms=rms))
        for peak, rms in zip(
            self._output_meter_peak_levels,
            self._output_meter_rms_levels,
            ):
            output_meter_levels.append(dict(peak=peak, rms=rms))
        result = {
            'server_meters': {
                'input_meter_levels': self._input_meter_levels,
                'output_meter_levels': self._output_meter_levels,
                },
            }
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def input_count(self):
        return self.server.server_options.input_bus_channel_count

    @property
    def output_count(self):
        return self.server.server_options.output_bus_channel_count

    @property
    def input_meter_command(self):
        return '/meter.inputs'

    @property
    def input_meter_synthdef(self):
        return self.make_meter_synthdef(
            channel_count=self.server.server_options.input_bus_channel_count,
            initial_bus=self.server.server_options.output_bus_channel_count,
            command_name=self.input_meter_command,
            )

    @property
    def output_meter_command(self):
        return '/meter.outputs'

    @property
    def output_meter_synthdef(self):
        return self.make_meter_synthdef(
            channel_count=self.server.server_options.output_bus_channel_count,
            initial_bus=0,
            command_name=self.output_meter_command,
            )

    @property
    def server(self):
        return self._server
