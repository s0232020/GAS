class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedChain:
    def __init__(self):
        self.head = None
        self.length = 0

    def isEmpty(self):
        return self.length == 0

    def getLength(self):
        return self.length

    def retrieve(self, index):
        if self.isEmpty() or index < 1 or index > self.length:
            return (None, False)

        current = self.head
        for _ in range(index - 1):
            current = current.next

        return (current.data, True)

    def insert(self, index, data):
        if index < 1 or index > self.length + 1:
            return False

        new_node = Node(data)

        if self.isEmpty():
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next

            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node

            if index == 1:
                self.head = new_node

        self.length += 1
        return True

    def delete(self, index):
        if self.isEmpty() or index < 1 or index > self.length:
            return False

        current = self.head
        for _ in range(index - 1):
            current = current.next

        current.prev.next = current.next
        current.next.prev = current.prev

        if index == 1:
            self.head = current.next

        if self.length == 1:
            self.head = None

        self.length -= 1
        return True

    def save(self):
        if self.isEmpty():
            return []

        result = []
        current = self.head
        for _ in range(self.length):
            result.append(current.data)
            current = current.next

            if current == self.head:
                break

        return result

    def load(self, data):
        self.head = None
        self.length = 0

        for item in reversed(data):
            self.insert(1, item)