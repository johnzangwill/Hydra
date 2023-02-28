from tree import Node

def test_depth():
    trials = [
        (Node(), 0),
        (Node(Node(Node())), 2),
        (Node(Node(Node(), Node())), 2),
        (Node(Node(), Node(Node(Node())), Node()), 3),
    ]
    for hydra, depth in trials:
        assert hydra.get_depth() == depth

def test_chop_myself():
    doomed = Node()
    hydra = Node(Node(Node(doomed)))
    expected = Node(Node(Node(),Node(),Node()))

    doomed.chop_myself()
    assert str(hydra) == str(expected)