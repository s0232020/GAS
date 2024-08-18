class TreeItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"TreeItem(key={self.key}, value={self.value})"

class Node:
    def __init__(self):
        self.items = []
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.items) == 3

    def add(self, item):
        self.items.append(item)
        self.items.sort(key=lambda x: x.key)

    def split(self):
        mid_index = 1
        mid_item = self.items[mid_index]

        left_node = Node()
        left_node.items = self.items[:mid_index]
        left_node.children = self.children[:mid_index + 1]

        right_node = Node()
        right_node.items = self.items[mid_index + 1:]
        right_node.children = self.children[mid_index + 1:]

        return left_node, mid_item, right_node

class TwoThreeFourTree:
    def __init__(self):
        self.root = Node()

    def isEmpty(self):
        return len(self.root.items) == 0

    def insertItem(self, item):
        if self.isEmpty():
            self.root.items.append(item)
        else:
            if self.root.is_full():
                old_root = self.root
                self.root = Node()
                self.root.children.append(old_root)
                self._split_child(self.root, 0)
            self._insert_non_full(self.root, item)
        return True

    def _insert_non_full(self, node, item):
        if node.is_leaf():
            node.add(item)
        else:
            index = len(node.items) - 1
            while index >= 0 and item.key < node.items[index].key:
                index -= 1
            index += 1
            if node.children[index].is_full():
                self._split_child(node, index)
                if item.key > node.items[index].key:
                    index += 1
            self._insert_non_full(node.children[index], item)

    def _split_child(self, parent, index):
        node = parent.children[index]
        left_node, mid_item, right_node = node.split()
        parent.items.insert(index, mid_item)
        parent.children[index] = left_node
        parent.children.insert(index + 1, right_node)

    def retrieveItem(self, key):
        return self._retrieve(self.root, key)

    def _retrieve(self, node, key):
        i = 0
        while i < len(node.items) and key > node.items[i].key:
            i += 1
        if i < len(node.items) and key == node.items[i].key:
            return node.items[i].value, True
        elif node.is_leaf():
            return None, False
        else:
            return self._retrieve(node.children[i], key)

    def inorderTraverse(self, func):
        self._inorder_traverse(self.root, func)

    def _inorder_traverse(self, node, func):
        for i in range(len(node.items)):
            if i < len(node.children):
                self._inorder_traverse(node.children[i], func)
            func(node.items[i].key)
        if node.children:
            self._inorder_traverse(node.children[-1], func)

    def deleteItem(self, key):
        result = self._delete(self.root, key)
        if not self.root.items and self.root.children:
            self.root = self.root.children[0]
        return result

    def _merge_children(self, parent, index):
        child = parent.children[index]
        sibling = parent.children.pop(index + 1)
        child.items.append(parent.items.pop(index))
        child.items.extend(sibling.items)
        if not sibling.is_leaf():
            child.children.extend(sibling.children)
        if not parent.items and parent == self.root:
            self.root = child

    def _delete(self, node, key):
        def redistribute(node, index):
            if index > 0:  # borrow from the previous sibling
                node.children[index].items.insert(0, node.items[index - 1])
                node.items[index - 1] = node.children[index - 1].items.pop()
                if not node.children[index - 1].is_leaf():
                    node.children[index].children.insert(0, node.children[index - 1].children.pop())
            else:  # borrow from the next sibling
                node.children[index].items.append(node.items[index])
                node.items[index] = node.children[index + 1].items.pop(0)
                if not node.children[index + 1].is_leaf():
                    node.children[index].children.append(node.children[index + 1].children.pop(0))

        i = 0
        while i < len(node.items) and key > node.items[i].key:
            i += 1

        if i < len(node.items) and key == node.items[i].key:
            if node.is_leaf():
                del node.items[i]
                return True
            else:
                if len(node.children[i].items) >= 2:
                    predecessor = self._get_max(node.children[i])
                    node.items[i] = predecessor
                    self._delete(node.children[i], predecessor.key)
                    return True
                elif i + 1 < len(node.children) and len(node.children[i + 1].items) >= 2:
                    successor = self._get_min(node.children[i + 1])
                    node.items[i] = successor
                    self._delete(node.children[i + 1], successor.key)
                    return True
                else:
                    if i < len(node.items) - 1:
                        self._merge_children(node, i)
                    else:
                        self._merge_children(node, i - 1)
                    if not node.is_leaf():  # Only call _delete again if the node is not a leaf
                        return self._delete(node, key)  # Check the root again after merging
        elif not node.is_leaf():
            if len(node.children[i].items) < 2:
                if i > 0 and len(node.children[i - 1].items) >= 2:
                    redistribute(node, i)
                elif i < len(node.items) and len(node.children[i + 1].items) >= 2:
                    redistribute(node, i + 1)
                else:
                    if i < len(node.items):
                        self._merge_children(node, i)
                    else:
                        self._merge_children(node, i - 1)
                return self._delete(node, key)  # Check the root again after merging
            if i < len(node.children):
                return self._delete(node.children[i], key)
        return False

    def _get_max(self, node):
        while not node.is_leaf():
            node = node.children[-1]
        return node.items[-1]

    def _get_min(self, node):
        while not node.is_leaf():
            node = node.children[0]
        return node.items[0]

    def _borrow_from_prev(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index - 1]

        child.items.insert(0, parent.items[index - 1])
        if not sibling.is_leaf():
            child.children.insert(0, sibling.children.pop())
        parent.items[index - 1] = sibling.items.pop()

    def _borrow_from_next(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]

        child.items.append(parent.items[index])
        if not sibling.is_leaf():
            child.children.append(sibling.children.pop(0))
        parent.items[index] = sibling.items.pop(0)

    def save(self):
        return self._save(self.root)

    def _save(self, node):
        data = {}
        data['root'] = [item.key for item in node.items]
        if node.children:
            data['children'] = [self._save(child) for child in node.children]
        return data

    def load(self, data):
        def collect_items(node):
            items = node['root']
            if 'children' in node:
                for child in node['children']:
                    items.extend(collect_items(child))
            return items

        items = collect_items(data)
        self.root = Node()
        for item in items:
            self.insertItem(TreeItem(item, item))

    def _load(self, data):
        node = Node()
        node.items = [TreeItem(key, key) for key in data['root']]
        if 'children' in data:
            node.children = [self._load(child) for child in data['children']]
        return node

def createTreeItem(key, value):
    return TreeItem(key, value)

class TwoThreeFourTreeTable:
    def __init__(self):
        self.tree = TwoThreeFourTree()

    def tableIsEmpty(self):
        return self.tree.isEmpty()

    def tableInsert(self, item):
        return self.tree.insertItem(item)

    def tableRetrieve(self, key):
        return self.tree.retrieveItem(key)

    def traverseTable(self, func):
        self.tree.inorderTraverse(func)

    def tableDelete(self, key):
        return self.tree.deleteItem(key)

    def save(self):
        return self.tree.save()

    def load(self, data):
        self.tree.load(data)
