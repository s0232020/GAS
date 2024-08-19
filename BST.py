class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root is None

    def searchTreeInsert(self, node):
        if self.isEmpty():
            self.root = node
            return True
        return self._insert(self.root, node)

    def _insert(self, current, node):
        if node.key == current.key:
            return False  # Duplicate key not allowed
        elif node.key < current.key:
            if current.left is None:
                current.left = node
                return True
            else:
                return self._insert(current.left, node)
        else:
            if current.right is None:
                current.right = node
                return True
            else:
                return self._insert(current.right, node)

    def searchTreeRetrieve(self, key):
        return self._retrieve(self.root, key)

    def _retrieve(self, current, key):
        if current is None:
            return (None, False)
        elif key == current.key:
            return (current.value, True)
        elif key < current.key:
            return self._retrieve(current.left, key)
        else:
            return self._retrieve(current.right, key)

    def inorderTraverse(self, callback):
        self._inorderTraverse(self.root, callback)

    def _inorderTraverse(self, current, callback):
        if current is not None:
            self._inorderTraverse(current.left, callback)
            callback(current.key)
            self._inorderTraverse(current.right, callback)

    def searchTreeDelete(self, key):
        return self._delete(None, self.root, key)

    def _delete(self, parent, current, key):
        if current is None:
            return False

        if key == current.key:
            if current.left is None and current.right is None:
                if parent is None:
                    self.root = None
                elif parent.left == current:
                    parent.left = None
                else:
                    parent.right = None
            elif current.left is None:
                if parent is None:
                    self.root = current.right
                elif parent.left == current:
                    parent.left = current.right
                else:
                    parent.right = current.right
            elif current.right is None:
                if parent is None:
                    self.root = current.left
                elif parent.left == current:
                    parent.left = current.left
                else:
                    parent.right = current.left
            else:
                successor_parent = current
                successor = current.right
                while successor.left is not None:
                    successor_parent = successor
                    successor = successor.left

                current.key, current.value = successor.key, successor.value
                self._delete(successor_parent, successor, successor.key)

            return True
        elif key < current.key:
            return self._delete(current, current.left, key)
        else:
            return self._delete(current, current.right, key)

    def save(self):
        return self._save(self.root)

    def _save(self, current):
        if current is None:
            return None

        left_child = self._save(current.left)
        right_child = self._save(current.right)

        if left_child is not None and right_child is not None:
            return {'root': current.key, 'children': [left_child, right_child]}
        elif left_child is not None:
            return {'root': current.key, 'children': [left_child, None]}
        elif right_child is not None:
            return {'root': current.key, 'children': [None, right_child]}
        else:
            return {'root': current.key}

    def load(self, data):
        self.root = self._load(data)

    def _load(self, data):
        if data is None:
            return None
        node = TreeNode(data['root'], data['root'])
        if 'children' in data and data['children'] is not None:
            node.left = self._load(data['children'][0])
            node.right = self._load(data['children'][1])
        return node

def createTreeItem(key, value):
    return TreeNode(key, value)