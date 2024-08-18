def createTreeItem(key, value):
    return (key, value)

class Node:
    def __init__(self, keys=None, children=None):
        self.keys = keys if keys else []
        self.children = children if children else []

    def is_leaf(self):
        return len(self.children) == 0

class TwoThreeTree:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root is None

    def insertItem(self, item):
        if not self.root:
            self.root = Node(keys=[item[0]])
            return True
        else:
            self._insert(self.root, item[0])
            if len(self.root.keys) == 3:
                self._split_root()
            return True

    def _insert(self, node, key):
        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1

        if node.is_leaf():
            node.keys.insert(index, key)
        else:
            self._insert(node.children[index], key)
            if len(node.children[index].keys) > 2:
                self._split_child(node, index)

        if len(node.keys) > 2 and node is self.root:
            self._split_root()

    def _split_root(self):
        median = len(self.root.keys) // 2
        left_keys = self.root.keys[:median]
        right_keys = self.root.keys[median + 1:]
        middle_key = self.root.keys[median]

        left_child = Node(keys=left_keys, children=self.root.children[:median + 1])
        right_child = Node(keys=right_keys, children=self.root.children[median + 1:])

        self.root = Node(keys=[middle_key], children=[left_child, right_child])

    def _split_child(self, parent, index):
        node = parent.children[index]
        median = len(node.keys) // 2
        left_keys = node.keys[:median]
        right_keys = node.keys[median + 1:]
        middle_key = node.keys[median]

        left_child = Node(keys=left_keys, children=node.children[:median + 1])
        right_child = Node(keys=right_keys, children=node.children[median + 1:])

        parent.children[index] = left_child
        parent.children.insert(index + 1, right_child)
        parent.keys.insert(index, middle_key)

    def retrieveItem(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return (None, False)
        if key in node.keys:
            return (key, True)
        if node.is_leaf():
            return (None, False)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            return self._search(node.children[i], key)

    def save(self):
        return self._save(self.root)

    def _save(self, node):
        if not node:
            return None
        if node.is_leaf():
            return {'root': node.keys}
        else:
            children_data = []
            for child in node.children:
                children_data.append(self._save(child))
            return {'root': node.keys, 'children': children_data}

    def load(self, tree_dict):
        self.root = self._load_node(tree_dict)
        return self

    def _load_node(self, node_dict):
        if not node_dict:
            return None
        node = Node(keys=node_dict['root'])
        if 'children' in node_dict:
            node.children = [self._load_node(child) for child in node_dict['children']]
        return node

    def deleteItem(self, key):
        if not self.root or not self._search(self.root, key)[1]:
            return False
        else:
            deleted = self._delete(self.root, key)
            if not self.root.keys and self.root.children:
                self.root = self.root.children[0]
            if self.root and not self.root.keys and not self.root.children:
                self.root = None
            return deleted

    def _delete(self, node, key):
        if key in node.keys:
            index = node.keys.index(key)
            if node.is_leaf():
                node.keys.remove(key)
                return True
            else:
                if len(node.children[index].keys) >= 2 or len(node.children[index + 1].keys) >= 2:
                    if len(node.children[index].keys) >= 2:
                        predecessor = self._get_predecessor(node.children[index])
                        pred_key = predecessor.keys[-1]
                        node.keys[index] = pred_key
                        return self._delete(node.children[index], pred_key)
                    else:
                        successor = self._get_successor(node.children[index + 1])
                        succ_key = successor.keys[0]
                        node.keys[index] = succ_key
                        return self._delete(node.children[index + 1], succ_key)
                else:
                    self._merge(node, index)
                    return self._delete(node, key)
        else:
            if node.is_leaf():
                return False

            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if len(node.children[i].keys) == 1:
                if i > 0 and len(node.children[i - 1].keys) > 1:
                    self._borrow_from_left(node, i)
                elif i < len(node.children) - 1 and len(node.children[i + 1].keys) > 1:
                    self._borrow_from_right(node, i)
                else:
                    if i > 0:
                        self._merge(node, i - 1)
                    else:
                        self._merge(node, i)
                    if len(node.keys) == 0 and node == self.root:
                        self.root = node.children[0]

                # Check if the key exists in the child node before deleting it
            if self._search(node.children[i], key)[1]:
                return self._delete(node.children[i], key)
            else:
                return False

    def _split_node(self, parent, index):  # New method
        node = parent.children[index]
        median = len(node.keys) // 2
        left_keys = node.keys[:median]
        right_keys = node.keys[median + 1:]
        middle_key = node.keys[median]

        left_child = Node(keys=left_keys, children=node.children[:median + 1])
        right_child = Node(keys=right_keys, children=node.children[median + 1:])

        parent.children[index] = left_child
        parent.children.insert(index + 1, right_child)
        parent.keys.insert(index, middle_key)

    def _borrow_from_left(self, node, index):
        left_child = node.children[index - 1]
        target_child = node.children[index]
        target_child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = left_child.keys.pop(-1)
        if left_child.children:
            target_child.children.insert(0, left_child.children.pop(-1))

    def _borrow_from_right(self, node, index):
        right_child = node.children[index + 1]
        target_child = node.children[index]
        target_child.keys.append(node.keys[index])
        node.keys[index] = right_child.keys.pop(0)
        if right_child.children:
            target_child.children.append(right_child.children.pop(0))

    def _merge(self, node, index):
        target_child = node.children[index]
        sibling = node.children.pop(index + 1)

        if node.keys:  # Check if node.keys is not empty
            target_child.keys.append(node.keys.pop(index))
        target_child.keys.extend(sibling.keys)
        target_child.children.extend(sibling.children)

        # Sort the keys after merging
        target_child.keys.sort()

        # If node becomes empty and it's the root, adjust the root
        if not node.keys and node == self.root:
            self.root = target_child

    def _get_predecessor(self, node):
        if node.is_leaf():
            return node
        else:
            return self._get_predecessor(node.children[-1])

    def _get_successor(self, node):
        if node.is_leaf():
            return node
        else:
            return self._get_successor(node.children[0])

    def inorderTraverse(self, action):
        if self.root:
            self._inorder_traverse(self.root, action)

    def _inorder_traverse(self, node, action):
        if node:
            for i in range(len(node.keys)):
                if node.children and len(node.children) > i:
                    self._inorder_traverse(node.children[i], action)
                action(node.keys[i])
            if node.children and len(node.children) > len(node.keys):
                self._inorder_traverse(node.children[-1], action)

class TwoThreeTreeTable:
    def __init__(self):
        self.tree = TwoThreeTree()

    def tableIsEmpty(self):
        return self.tree.isEmpty()

    def tableInsert(self, item):
        return self.tree.insertItem(item)

    def tableRetrieve(self, key):
        return self.tree.retrieveItem(key)

    def tableDelete(self, key):
        return self.tree.deleteItem(key)

    def save(self):
        return self.tree.save()

    def load(self, tree_dict):
        self.tree.load(tree_dict)

    def traverseTable(self, action):
        self.tree.inorderTraverse(action)