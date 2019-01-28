from supriya.realtime.Group import Group


class RootNode(Group):

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, server=None):
        super().__init__()
        self._server = server

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        node = super()._as_graphviz_node()
        node.attributes["fillcolor"] = "lightsalmon2"
        return node

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass

    def run(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return 0

    @property
    def parent(self):
        return None
