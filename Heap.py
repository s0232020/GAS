from collections import deque
class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def heapIsEmpty(self):
        return self.size == 0

    def destroyHeap(self):
        self.heap = []
        self.size = 0

    def heapInsert(self, key):
        self.heap.append(key)
        self.size += 1
        self.trickle_up(self.size - 1)
        return True

    def heapDelete(self):
        if self.heapIsEmpty():
            return (None, False)
        else:
            deleted = self.heap[0]
            self.heap[0] = self.heap[self.size - 1]
            self.size -= 1
            self.heap.pop()
            self.trickle_down(0)
            return (deleted, True)

    def trickle_down(self, pos):
        newitem = self.heap[pos]
        left_child_pos = 2 * pos + 1
        right_child_pos = 2 * pos + 2

        max_pos = pos

        if left_child_pos < self.size and self.heap[left_child_pos] > self.heap[max_pos]:
            max_pos = left_child_pos

        if right_child_pos < self.size and self.heap[right_child_pos] > self.heap[max_pos]:
            max_pos = right_child_pos

        if max_pos != pos:
            self.heap[pos], self.heap[max_pos] = self.heap[max_pos], self.heap[pos]
            self.trickle_down(max_pos)

    def trickle_up(self, pos):
        while pos > 0:
            parent_pos = (pos - 1) // 2
            if self.heap[pos] > self.heap[parent_pos]:
                self.heap[pos], self.heap[parent_pos] = self.heap[parent_pos], self.heap[pos]
                pos = parent_pos
            else:
                break

    def save(self):
        def format_node(idx):
            if idx >= self.size:
                return None
            node = {'root': self.heap[idx]}
            left_child_idx = 2 * idx + 1
            right_child_idx = 2 * idx + 2
            left_child = format_node(left_child_idx)
            right_child = format_node(right_child_idx)
            if left_child is not None or right_child is not None:
                node['children'] = [left_child, right_child]
            return node

        return format_node(0)

    def load(self, tree):
        def bfs_collect_items(node):
            queue = deque([node])
            items = []
            while queue:
                node = queue.popleft()
                if node is not None:
                    items.append(node['root'])
                    if 'children' in node:
                        for child in node['children']:
                            queue.append(child)
            return items

        self.destroyHeap()
        items = bfs_collect_items(tree)
        for item in items:
            self.heapInsert(item)

    def __repr__(self):
        return str(self.heap)

class HeapQueue:
    def __init__(self):
        self.queue = Heap()

    def isEmpty(self):
        return self.queue.heapIsEmpty()

    def enqueue(self, item):
        return self.queue.heapInsert(item)

    def dequeue(self):
        if self.isEmpty():
            return (None, False)
        else:
            return self.queue.heapDelete()

    def save(self):
        return self.queue.save()

    def load(self, tree):
        self.queue.load(tree)

    def __repr__(self):
        return str(self.queue.heap)
