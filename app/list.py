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
        self.first = None
        self.last = None
    
    def push_left(self, value):
        if self.first is None:
            self.first = self.last = ListNode(value, None, None)
        else:
            node = ListNode(value, None, self.first)
            self.first = node

    def push_right(self, value):
        if self.first is None:
            self.first = self.last = ListNode(value, None, None)
        else:
            self.last.next = ListNode(value, self.last, None)
            self.last = self.last.next

    def pop_left(self):
        if self.first is None:
            return None
        elif self.first is self.last:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next

    def pop_right(self):
        if self.last is None:
            return None
        elif self.first is self.last:
            self.first = None
            self.last = None
        else:
            self.last = self.last.previous

    def empty(self):
        return self.first is None

    def __iter__(self):
        node = self.first
        while node is not None:
            yield node.value
            node = node.next

    def __reversed__(self):
        node = self.last
        while node is not None:
            yield node.value
            node = node.previous

    def __repr__(self):
        values = ', '.join(list(map(str, self)))
        return f'[{values}]'

    @staticmethod
    def from_list(data):
        l = DoubleLinkedList()
        for element in data:
            l.push_right(element)
        
        return l
