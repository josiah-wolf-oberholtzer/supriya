import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class BufferFillRequest(Request):
    """
    A /b_fill request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferFillRequest(
        ...     buffer_id=23,
        ...     index_count_value_triples=(
        ...         (0, 8, 0.1),
        ...         (11, 4, 0.2),
        ...         ),
        ...     )
        >>> request
        BufferFillRequest(
            buffer_id=23,
            index_count_value_triples=(
                (0, 8, 0.1),
                (11, 4, 0.2),
                ),
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_fill', 23, 0, 8, 0.1, 11, 4, 0.2)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_FILL

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_count_value_triples=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        triples = []
        for index, count, value in index_count_value_triples:
            triple = (int(index), int(count), float(value))
            triples.append(triple)
        triples = tuple(triples)
        self._index_count_value_triples = triples

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        for index, count, value in self.index_count_value_triples:
            contents.append(int(index))
            contents.append(int(count))
            contents.append(float(value))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples
