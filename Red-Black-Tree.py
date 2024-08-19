class TreeItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"TreeItem(key={self.key}, value={self.value})"

def createTreeItem(key, value):
    return TreeItem(key, value)

class Node:
    def __init__(self, key, val, color=True, left=None, right=None, parent=None):
        self.key = key
        self.val = val
        self.color = color  # True = red, False = black
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, None, False)
        self.root = self.NIL

    def insertItem(self, item):
        node = Node(item.key, item.value)
        node.left = self.NIL
        node.right = self.NIL
        node.color = True  # New nodes are red

        if self.root == self.NIL:
            # If the tree is empty, insert the first node and make it black
            self.root = node
            node.color = False  # The root must always be black
            return

        current = self.root
        parent = None

        # Traverse down the tree to find the insertion point
        while current != self.NIL:
            parent = current

            # Recolor and rotate if necessary before moving down
            if current.left.color and current.right.color:
                self.recolor_and_rotate(current)

            # Move down the tree
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node
        node.parent = parent
        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        # Fix potential violations caused by the insertion
        self.fix_insert(node)

    def recolor_and_rotate(self, node):
        # Recolor the current node and its children
        node.color = True
        if node.left != self.NIL:
            node.left.color = False
        if node.right != self.NIL:
            node.right.color = False

        # If the current node's parent is red, we may need to rotate
        if node.parent and node.parent.color:
            self.fix_insert(node)

    def fix_insert(self, node):
        while node != self.root and node.parent.color:  # While the parent is red
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color:  # Case 1: Uncle is red
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # Case 2: Node is a right child
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color:  # Case 1: Uncle is red
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # Case 2: Node is a left child
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.left_rotate(node.parent.parent)

        self.root.color = False  # The root must always be black

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



# Test the tree
t = RedBlackTree()
t.insertItem(createTreeItem(5, 5))
t.insertItem(createTreeItem(10, 10))
t.insertItem(createTreeItem(2, 2))
t.insertItem(createTreeItem(12, 12))
t.insertItem(createTreeItem(15, 15))
t.insertItem(createTreeItem(1, 1))
t.insertItem(createTreeItem(3, 3))
t.insertItem(createTreeItem(4, 4))
t.insertItem(createTreeItem(16, 16))
t.insertItem(createTreeItem(13, 13))
t.inorderTraverse(print)
print(t.save())
# {'root': 5, 'color': 'black', 'children': [{'root': 2, 'color': 'black', 'children': [{'root': 1, 'color': 'black'}, {'root': 3, 'color': 'black', 'children': [None, {'root': 4, 'color': 'red'}]}]}, {'root': 12, 'color': 'black', 'children': [{'root': 10, 'color': 'black'}, {'root': 15, 'color': 'black', 'children': [{'root': 13, 'color': 'red'}, {'root': 16, 'color': 'red'}]}]}]}
# {'root': 5, 'color': 'black', 'children': [{'root': 2, 'color': 'black', 'children': [{'root': 1, 'color': 'black'}, {'root': 3, 'color': 'black', 'children': [None, {'root': 4, 'color': 'red'}]}]}, {'root': 12, 'color': 'black', 'children': [{'root': 10, 'color': 'black'}, {'root': 15, 'color': 'black', 'children': [{'root': 13, 'color': 'red'}, {'root': 16, 'color': 'red'}]}]}]}