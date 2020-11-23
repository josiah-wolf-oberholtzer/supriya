import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class GroupDeepFreeRequest(Request):
    """
    A /g_deepFree request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> group = supriya.Group().allocate()
        >>> group.extend([supriya.Synth(), supriya.Group()])
        >>> group[1].extend([supriya.Synth(), supriya.Group()])
        >>> group[1][1].extend([supriya.Synth(), supriya.Group()])

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1002 group
                        1003 default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                        1004 group
                            1005 default
                                out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                            1006 group

    ::

        >>> request = supriya.commands.GroupDeepFreeRequest(group)
        >>> request.to_osc()
        OscMessage('/g_deepFree', 1000)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/g_deepFree', 1000))
        ('S', OscMessage('/sync', 2))
        ('R', OscMessage('/n_end', 1001, -1, -1, -1, 0))
        ('R', OscMessage('/n_end', 1003, -1, -1, -1, 0))
        ('R', OscMessage('/n_end', 1005, -1, -1, -1, 0))
        ('R', OscMessage('/synced', 2))

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1004 group
                            1006 group

    ::

        >>> print(server.query_local_nodes(True))
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1004 group
                            1006 group

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.GROUP_DEEP_FREE

    ### INITIALIZER ###

    def __init__(self, group_id):
        Request.__init__(self)
        self._group_id = group_id

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        group_id = int(self.group_id)
        message = supriya.osc.OscMessage(request_id, group_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def group_id(self):
        return self._group_id
