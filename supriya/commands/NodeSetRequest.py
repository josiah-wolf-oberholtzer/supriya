import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class NodeSetRequest(Request):
    """
    A /n_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeSetRequest(
        ...     1000,
        ...     frequency=443.1,
        ...     phase=0.5,
        ...     amplitude=0.1,
        ...     )
        >>> request
        NodeSetRequest(
            amplitude=0.1,
            frequency=443.1,
            node_id=1000,
            phase=0.5,
            )

    ::

        >>> request.to_osc()
        OscMessage('/n_set', 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_SET

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = kwargs

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = int(self.node_id)
        contents = [request_id, node_id]
        for key, value in sorted(self._kwargs.items()):
            contents.append(key)
            contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id
