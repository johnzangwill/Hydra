from ordinal import Ordinal

class Node:
    n = 2
    m = None
    i = 0

    def __init__(self, *args):
        if Node.m is None:
            Node.m = Node.n
        self.children = []
        self.parent = None
        self.add(*args)

    def reset(self):
        self.children = []
        Node.m = Node.n

    def add(self, *args):
        for node in args:
            node.parent = self
        self.children.extend(list(args))

    def __str__(self):
        if self.children:
            if len(self.children) > 15:
                return '...'
            else:
                children = ','.join(str(node) for node in self.children)
                return f'node({children})'
        if not self.parent:
            return 'orphan'
        return 'head'

    def is_head(self):
        return not self.children

    def count(self):
        if self.children:
            return sum(node.count() for node in self.children)
        return 1

    def copy(self):
        children = [node.copy() for node in self.children]
        return Node(*children)

    def chop_child(self):
        if not self.is_head():
            node = self.children[0]
            if node.is_head():
                node.chop_myself()
            else:
                node.chop_child()

    def chop_myself(self):
        if self.is_head():
            Node.m += Node.i
            parent = self.parent
            if parent:
                parent.children.remove(self)
                if parent.parent:
                    copies = [parent.copy() for _ in range(Node.m)]
                    parent.parent.add(*copies)
            else:
                raise Exception('not child')
        else:
            raise Exception('not head')

    def get_height(self):
        if self.children:
            return 1 + max(child.get_height() for child in self.children)

        return 0

    def get_ordinal(self):
        args = [child.get_ordinal() for child in self.children]
        return Ordinal(*args)
        
