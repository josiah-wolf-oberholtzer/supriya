# -*- encoding: utf-8 -*-
import collections
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class State(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_transitions',
        '_nodes_to_children',
        '_nodes_to_parents',
        '_offset',
        '_session',
        '_start_buffers',
        '_start_nodes',
        '_stop_buffers',
        '_stop_nodes',
        )

    _ordered_buffer_request_types = (
        requesttools.BufferZeroRequest,
        )

    ### INITIALIZER ###

    def __init__(self, session, offset):
        SessionObject.__init__(self, session)
        self._transitions = collections.OrderedDict()
        self._nodes_to_children = None
        self._nodes_to_parents = None
        self._start_nodes = set()
        self._stop_nodes = set()
        self._start_buffers = set()
        self._stop_buffers = set()
        self._offset = offset

    ### SPECIAL METHODS ###

    def __graph__(self, include_controls=False):
        from supriya.tools import nonrealtimetools
        return nonrealtimetools.StateGrapher.graph(
            self,
            include_controls=include_controls,
            )

    def __repr__(self):
        return '<{} @{!r}>'.format(
            type(self).__name__,
            self.offset,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _apply_transitions(
        cls,
        transitions=None,
        nodes_to_children=None,
        nodes_to_parents=None,
        stop_nodes=None,
        ):
        from supriya.tools import nonrealtimetools
        if nodes_to_children is not None:
            nodes_to_children = nodes_to_children.copy()
        else:
            nodes_to_children = {}
        if nodes_to_parents is not None:
            nodes_to_parents = nodes_to_parents.copy()
        else:
            nodes_to_parents = {}
        transitions = transitions or {}
        for node, action in transitions.items():
            action.apply_transform(nodes_to_children, nodes_to_parents)
        stop_nodes = stop_nodes or ()
        for stop_node in stop_nodes:
            nonrealtimetools.NodeAction.free_node(
                stop_node, nodes_to_children, nodes_to_parents)
        return nodes_to_children, nodes_to_parents

    def _clone(self, new_offset):
        if float('-inf') < self.offset:
            self.session._apply_transitions(self.offset, chain=False)
        state = type(self)(
            self.session,
            new_offset,
            )
        state._nodes_to_children = self.nodes_to_children.copy()
        state._nodes_to_parents = self.nodes_to_parents.copy()
        if new_offset == self.offset:
            state._transitions = self._transitions.copy()
            state._start_buffers.update(self.start_buffers)
            state._stop_buffers.update(self.stop_buffers)
            state._start_nodes.update(self.start_nodes)
            state._stop_nodes.update(self.stop_nodes)
        return state

    def _collect_buffer_requests(
        self,
        id_mapping,
        buffer_settings,
        start_buffers,
        stop_buffers,
        ):
        requests = []
        if start_buffers:
            for buffer_ in sorted(start_buffers, key=lambda x: x.session_id):
                request = requesttools.BufferAllocateRequest(
                    buffer_id=id_mapping[buffer_],
                    channel_count=buffer_.channel_count,
                    frame_count=buffer_.frame_count,
                    )
                requests.append(request)
        buffer_settings = buffer_settings.get(self.offset)
        if buffer_settings:
            for request_type in self._ordered_buffer_request_types:
                if request_type in buffer_settings:
                    requests.extend(buffer_settings[request_type])
        if stop_buffers:
            for buffer_ in sorted(stop_buffers, key=lambda x: x.session_id):
                request = requesttools.BufferFreeRequest(
                    buffer_id=id_mapping[buffer_],
                    )
                requests.append(request)
        return requests

    def _collect_buffers(self, force_stop):
        start_buffers = self.start_buffers
        stop_buffers = self.stop_buffers
        if force_stop:
            stop_buffers.update(
                self.session._buffers.find_timespans_overlapping_offset(
                    self.offset))
        return start_buffers, stop_buffers

    def _collect_bus_requests(self, bus_settings):
        requests = []
        if self.offset in bus_settings:
            index_value_pairs = sorted(bus_settings[self.offset].items())
            request = requesttools.ControlBusSetRequest(
                index_value_pairs=index_value_pairs,
                )
            requests.append(request)
        return requests

    def _collect_node_action_requests(self, id_mapping, node_settings, start_nodes, node_actions):
        from supriya.tools import nonrealtimetools
        requests = []
        for source, action in node_actions.items():
            if source in start_nodes:
                if isinstance(source, nonrealtimetools.Synth):
                    synth_kwargs = {}
                    if source in node_settings:
                        synth_kwargs.update(node_settings.pop(source))
                    if 'duration' in source.synthdef.parameter_names:
                        # need to propagate in session rendering timespan
                        # as many nodes have "infinite" duration
                        synth_kwargs['duration'] = float(source.duration)
                    request = source.to_request(action, id_mapping, **synth_kwargs)
                else:
                    request = source.to_request(action, id_mapping)
            else:
                request = action.to_request(id_mapping)
            requests.append(request)
        return requests

    def _collect_node_set_requests(self, id_mapping, node_settings):
        from supriya.tools import nonrealtimetools
        requests = []
        bus_prototype = (
            nonrealtimetools.Bus,
            nonrealtimetools.BusGroup,
            type(None),
            )
        buffer_prototype = (
            nonrealtimetools.Buffer,
            nonrealtimetools.BufferGroup,
            )
        for node, settings in node_settings.items():
            node_id = id_mapping[node]
            a_settings = {}
            c_settings = {}
            n_settings = {}
            for key, value in settings.items():
                if isinstance(value, bus_prototype):
                    if value is None:
                        c_settings[key] = -1
                    elif value.calculation_rate == servertools.CalculationRate.CONTROL:
                        c_settings[key] = id_mapping[value]
                    else:
                        a_settings[key] = id_mapping[value]
                else:
                    if isinstance(value, buffer_prototype):
                        value = id_mapping[value]
                    n_settings[key] = value
                if n_settings:
                    request = requesttools.NodeSetRequest(
                        node_id=node_id,
                        **n_settings
                        )
                    requests.append(request)
                if a_settings:
                    request = requesttools.NodeMapToAudioBusRequest(
                        node_id=node_id,
                        **a_settings
                        )
                    requests.append(request)
                if c_settings:
                    request = requesttools.NodeMapToControlBusRequest(
                        node_id=node_id,
                        **c_settings
                        )
                    requests.append(request)
            # separate out floats, control buses and audio buses
        return requests

    def _collect_nodes(self, force_stop):
        start_nodes = self.start_nodes
        stop_nodes = self.stop_nodes
        if force_stop:
            nonroot_nodes = set(
                node for node in self._iterate_nodes(
                    self.session.root_node,
                    self.nodes_to_children,
                    )
                if node is not self.session.root_node
                )
            stop_nodes.update(nonroot_nodes)
        return start_nodes, stop_nodes

    def _collect_node_settings(self):
        result = collections.OrderedDict()
        if self.nodes_to_children is None:
            # Current state is sparse;
            # Use previous non-sparse state's nodes to order settings.
            state = self.session._find_state_before(
                self.offset,
                with_node_tree=True,
                )
            iterator = self._iterate_nodes(
                self.session.root_node,
                state.nodes_to_children,
                )
        else:
            iterator = self._iterate_nodes(
                self.session.root_node,
                self.nodes_to_children,
                )
        for node in iterator:
            settings = node._collect_settings(self.offset)
            if settings:
                result[node] = settings
        return result

    def _collect_node_stop_requests(self, id_mapping, stop_nodes):
        requests = []
        if stop_nodes:
            free_ids, gate_ids = [], []
            for node in stop_nodes:
                node_id = id_mapping[node]
                if hasattr(node, 'synthdef') and \
                    'gate' in node.synthdef.parameter_names:
                    gate_ids.append(node_id)
                else:
                    free_ids.append(node_id)
            free_ids.sort()
            gate_ids.sort()
            if free_ids:
                request = requesttools.NodeFreeRequest(node_ids=free_ids)
                requests.append(request)
            if gate_ids:
                for node_id in gate_ids:
                    request = requesttools.NodeSetRequest(
                        node_id=node_id,
                        gate=0,
                        )
                    requests.append(request)
        return requests

    def _collect_synthdef_requests(self, visited_synthdefs, start_nodes):
        from supriya.tools import nonrealtimetools
        requests = []
        synthdefs = set()
        for node in start_nodes:
            if not isinstance(node, nonrealtimetools.Synth):
                continue
            elif node.synthdef in visited_synthdefs:
                continue
            synthdefs.add(node.synthdef)
            visited_synthdefs.add(node.synthdef)
        synthdefs = sorted(synthdefs, key=lambda x: x.anonymous_name)
        if synthdefs:
            request = requesttools.SynthDefReceiveRequest(synthdefs=synthdefs)
            requests.append(request)
        return requests

    def _desparsify(self):
        if self._nodes_to_children is not None:
            return
        previous_state = self.session._find_state_before(
            self.offset,
            with_node_tree=True,
            )
        self._nodes_to_children = previous_state.nodes_to_children.copy()
        self._nodes_to_parents = previous_state.nodes_to_parents.copy()

    def _sparsify(self):
        if self.is_sparse:
            self.session._remove_state_at(self.offset)

    @classmethod
    def _find_first_inconsistency(
        cls,
        root_node,
        nodes_to_children_one,
        nodes_to_children_two,
        stop_nodes,
        ):
        from supriya.tools import nonrealtimetools
        for parent in cls._iterate_nodes(root_node, nodes_to_children_one):
            if parent in stop_nodes:
                continue
            children_one = nodes_to_children_one.get(parent) or ()
            children_one = [
                node for node in children_one
                if node not in stop_nodes
                ]
            children_two = nodes_to_children_two.get(parent) or ()
            if children_one == children_two or not children_two:
                continue
            for i, child in enumerate(children_two):
                if not children_one:
                    action = 'ADD_TO_HEAD'
                    target = parent
                elif len(children_one) <= i:
                    action = 'ADD_AFTER'
                    target = children_one[i - 1]
                elif children_one[i] is not child:
                    action = 'ADD_BEFORE'
                    target = children_one[i]
                else:
                    continue
                transition = nonrealtimetools.NodeAction(
                    source=child,
                    target=target,
                    action=action,
                    )
                return transition

    @classmethod
    def _iterate_nodes(cls, root_node, nodes_to_children):
        def recurse(parent):
            yield parent
            children = nodes_to_children.get(parent, ()) or ()
            for child in children:
                for node in recurse(child):
                    yield node
        return recurse(root_node)

    @classmethod
    def _iterate_node_pairs(cls, root_node, nodes_to_children):
        def recurse(parent):
            children = nodes_to_children.get(parent, ()) or ()
            for child in children:
                yield parent, child
                for pair in recurse(child):
                    yield pair
        return recurse(root_node)

    @classmethod
    def _rebuild_transitions(cls, state_one, state_two):
        assert state_one.session.root_node is state_two.session.root_node
        a_children = state_one.nodes_to_children.copy()
        a_parents = state_one.nodes_to_parents.copy()
        b_children, b_parents = a_children.copy(), a_parents.copy()
        stop_nodes = state_two.stop_nodes
        transitions = collections.OrderedDict()
        counter = 0
        while (b_children != state_two.nodes_to_children):
            transition = State._find_first_inconsistency(
                state_one.session.root_node,
                b_children,
                state_two.nodes_to_children,
                stop_nodes,
                )
            if transition is not None:
                transitions[transition.source] = transition
            b_children, b_parents = State._apply_transitions(
                transitions, a_children, a_parents, stop_nodes,
                )
            counter += 1
            if counter == 10:
                raise Exception
        return transitions

    ### PUBLIC METHODS ###

    def report(self):
        state = {}
        node_hierarchy = {}
        items = sorted(self.nodes_to_children.items(),
            key=lambda item: item[0].session_id)
        for parent, children in items:
            if not children:
                children = []
            node_hierarchy[str(parent)] = [str(child) for child in children]
        node_lifecycle = {}
        if self.start_nodes:
            node_lifecycle['start'] = sorted(str(node) for node in self.start_nodes)
        if self.stop_nodes:
            node_lifecycle['stop'] = sorted(str(node) for node in self.stop_nodes)
        if node_hierarchy:
            state['hierarchy'] = node_hierarchy
        if node_lifecycle:
            state['lifecycle'] = node_lifecycle
        state['offset'] = self.offset
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def is_sparse(self):
        if self.start_nodes:
            return False
        elif self.stop_nodes:
            return False
        elif self.transitions:
            return False
        return True

    @property
    def nodes_to_children(self):
        return self._nodes_to_children

    @property
    def nodes_to_parents(self):
        return self._nodes_to_parents

    @property
    def offset(self):
        return self._offset

    @property
    def start_buffers(self):
        return self._start_buffers

    @property
    def start_nodes(self):
        return self._start_nodes

    @property
    def stop_buffers(self):
        return self._stop_buffers

    @property
    def stop_nodes(self):
        return self._stop_nodes

    @property
    def overlap_nodes(self):
        nodes = self.session._nodes
        return nodes.find_timespans_overlapping_offset(self.offset)

    @property
    def overlap_buffers(self):
        buffers = self.session._buffers
        return buffers.find_timespans_overlapping_offset(self.offset)

    @property
    def transitions(self):
        return self._transitions