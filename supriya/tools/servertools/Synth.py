from supriya.tools.servertools.Node import Node


class Synth(Node):
    r'''A synth.

    ::

        >>> from supriya import servertools
        >>> from supriya import synthdeftools
        >>> server = servertools.Server().boot()

    ::

        >>> synthdef = synthdeftools.SynthDef('test', frequency=440)
        >>> controls = synthdef.controls
        >>> sin_osc = synthdeftools.SinOsc.ar(
        ...     frequency=controls['frequency'],
        ...     ) * 0.0
        >>> out = synthdeftools.Out.ar(bus=(0, 1), source=sin_osc)
        >>> synthdef.add_ugen(out)
        >>> with servertools.WaitForServer('/synced', (1000,)):
        ...     synthdef.allocate()
        ...     server.send_message(('/sync', 1000))
        ...
        RECV: OscMessage('/done', '/d_recv')
        RECV: OscMessage('/synced', 1000)

    ::

        >>> synth = servertools.Synth(synthdef=synthdef).allocate()

    ::

        >>> server = server.quit()
        RECV: OscMessage('/done', '/quit')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef,
        ):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        Node.__init__(self)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        target_node=None,
        **kwargs
        ):
        from supriya.tools import servertools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            target_node=target_node,
            )
        message = servertools.CommandManager.make_synth_new_message(
            add_action=add_action,
            node_id=node_id,
            synthdef_name=self.synthdef.name,
            target_node_id=target_node_id,
            **kwargs
            )
        self.server.send_message(message)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
