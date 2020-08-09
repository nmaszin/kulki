class DoubleLinkedListNode:
    def __init__(self, value, previous, next):
        self.value = value
        self.previous = previous
        self.next = next
    
    def has_next(self):
        return self.next is not None
    
    def has_previous(self):
        return self.previous is not None

class DoubleLinkedList:
    def __init__(self):
        self.first_node = None
        self.last_node = None
    
    def push_first(self, value):
        if self.first_node is None:
            self.first_node = self.last_node = DoubleLinkedListNode(value, None, None)
        else:
            self.first_node = DoubleLinkedListNode(value, None, self.first_node)
            self.first_node.next.previous = self.first_node

    def push_last(self, value):
        if self.first_node is None:
            self.first_node = self.last_node = DoubleLinkedListNode(value, None, None)
        else:
            self.last_node.next = DoubleLinkedListNode(value, self.last_node, None)
            self.last_node = self.last_node.next

    def pop_first(self):
        value = self.first()

        if self.first_node is None:
            return None
        elif self.first_node is self.last_node:
            self.first_node = None
            self.last_node = None
        else:
            self.first_node = self.first_node.next
            self.first_node.previous = None

        return value

    def pop_last(self):
        value = self.last()

        if self.last_node is None:
            return None
        elif self.first_node is self.last_node:
            self.first_node = None
            self.last_node = None
        else:
            self.last_node = self.last_node.previous
            self.last_node.next = None

        return value

    def first(self):
        return self.first_node.value

    def last(self):
        return self.last_node.value

    def iterator_first(self):
        return self.first_node
    
    def iterator_last(self):
        return self.last_node

    def empty(self):
        return self.first_node is None

    def __iter__(self):
        node = self.first_node
        while node is not None:
            yield node.value
            node = node.next

    def __reversed__(self):
        node = self.last_node
        while node is not None:
            yield node.value
            node = node.previous

    def __repr__(self):
        values = ', '.join(list(map(str, self)))
        return f'[{values}]'

    def __len__(self):
        counter = 0
        node = self.first_node
        while node is not None:
            node = node.next
            counter += 1
        return counter

    @staticmethod
    def from_list(data):
        l = DoubleLinkedList()
        for element in data:
            l.push_last(element)
        
        return l
