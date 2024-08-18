class TreeItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"TreeItem(key={self.key}, value={self.value})"

def createTreeItem(key, value):
    return TreeItem(key, value)

class Node:
    def __init__(self, key, val, color = True, left = None, right = None, parent = None):
        self.key = key
        self.val = val
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, None, False)
        self.root = self.NIL

    def insertItem(self, item):
        node = Node(item.key, item.value)
        node.parent = None
        node.item = item
        node.left = self.NIL
        node.right = self.NIL
        node.color = True  # new node must be red

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.item.key < x.item.key:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y is None:
            self.root = node
        elif node.item.key < y.item.key:
            y.left = node
        else:
            y.right = node

        # if new node is a root node, simply return
        if node.parent is None:
            node.color = False
            return

        # if the grandparent is None, simply return
        if node.parent.parent is None:
            return

        # Fix the tree
        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color:
                    u.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = False
                    k.parent.parent.color = True
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color:
                    u.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = False
                    k.parent.parent.color = True
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = False

    def save(self):
        return self._save(self.root)

    def _save(self, node):
        data = {}
        data['root'] = node.key
        data['color'] = 'red' if node.color else 'black'
        children = [None, None]
        if node.left and node.left != self.NIL:
            children[0] = self._save(node.left)
        if node.right and node.right != self.NIL:
            children[1] = self._save(node.right)
        if children[0] is not None or children[1] is not None:
            data['children'] = children
        return data

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:  # x is root
            self.root = y
        elif x == x.parent.left:  # x is left child
            x.parent.left = y
        else:  # x is right child
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:  # y is root
            self.root = x
        elif y == y.parent.right:  # y is right child
            y.parent.right = x
        else:  # y is left child
            y.parent.left = x
        x.right = y
        y.parent = x

    def inorderTraverse(self, func, node=None):
        if node is None:
            node = self.root
        if node != self.NIL:
            self.inorderTraverse(func, node.left)
            func(node.key)
            self.inorderTraverse(func, node.right)