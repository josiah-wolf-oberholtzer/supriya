import uqbar.strings

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):

    group_a = supriya.realtime.Group()
    group_a.allocate()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_a)
    group_b = supriya.realtime.Group()
    group_a.append(group_b)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_b)
    synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_b.append(synth_c)
    group_c = supriya.realtime.Group()
    group_b.append(group_c)
    synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query(False))
    assert server_state == uqbar.strings.normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1004 test
                        1005 group
                    1006 test
        """
    )

    assert [x for x in group_a] == [synth_a, group_b, synth_d]

    assert [x for x in group_b] == [synth_b, synth_c, group_c]

    assert [x for x in group_c] == []
