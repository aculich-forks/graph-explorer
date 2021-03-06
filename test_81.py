from query import Query
from app import build_graphs_from_targets
from target import Target


def test_nontrivial_implicit_aggregation():
    # we ultimately want 1 graph with 1 line for each server,
    # irrespective of the values of the other tags (n1 and n2)
    # and even whether or not the metrics have those tags at all.
    query = Query("")
    query['group_by'] = {}
    query['sum_by'] = {'n1': [''], 'n2': ['']}

    targets = {
        # web1 : one with and without n2
        'web1.a.a': {
            'id': 'web1.a.a',
            'tags': {
                'server': 'web1',
                'n1': 'a',
                'n2': 'a'
            }
        },
        'web1.a': {
            'id': 'web1.a',
            'tags': {
                'server': 'web1',
                'n1': 'a',
            }
        },
        # web 2: 2 different values of n2
        'web2.a.a': {
            'id': 'web2.a.a',
            'tags': {
                'server': 'web2',
                'n1': 'a',
                'n2': 'a'
            }
        },
        'web2.a.b': {
            'id': 'web2.a.b',
            'tags': {
                'server': 'web2',
                'n1': 'a',
                'n2': 'b'
            }
        },
        # web3: with and without n2, diff value for n1
        'web3.a.a': {
            'id': 'web3.a.a',
            'tags': {
                'server': 'web3',
                'n1': 'a',
                'n2': 'a'
            }
        },
        'web3.b': {
            'id': 'web3.b',
            'tags': {
                'server': 'web3',
                'n1': 'b'
            }
        }
    }
    from pprint import pprint
    for (k, v) in targets.items():
        v = Target(v)
        v.get_graph_info(group_by={})
        targets[k] = v
    graphs, _query = build_graphs_from_targets(targets, query)
    # TODO: there should be only 1 graph, containing 3 lines, with each 2 targets per server
    # i.e. something like this:
    expected = {
        'targets': {
            {'id': ['web1.a.a', 'web1.a']},
            {'id': ['web2.a.a', 'web2.a.b']},
            {'id': ['web3.a.a', 'web3.b']}
        }
    }

    print "Graphs:"
    for (k, v) in graphs.items():
        print "graph key"
        pprint(k)
        print "val:"
        pprint(v)
    assert expected == graphs
