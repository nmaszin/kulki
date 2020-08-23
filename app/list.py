class DoubleLinkedListNode:
    """
    Klasa reprezentuje pojedynczy węzeł dwukierunkowej listy łączonej
    """

    def __init__(self, value, previous, next):
        """
        W konstruktorze przekazujemy: wartość, wskaźnik poprzedniego oraz następnego elementu
        """

        self.value = value
        self.previous = previous
        self.next = next

    def has_next(self):
        """
        Metoda informuje, czy obecny węzeł posiada swojego następnika
        """

        return self.next is not None

    def has_previous(self):
        """
        Metoda informuje, czy obecny węzeł posiada swojego poprzednika
        """

        return self.previous is not None


class DoubleLinkedList:
    """
    Klasa reprezentuje dwukierunkową listę łączoną
    """

    def __init__(self):
        """
        Konstruktor klasy
        """

        self.first_node = None
        self.last_node = None

    def push_first(self, value):
        """
        Metoda dodaje jeden element do listy, z jej lewej strony
        """

        if self.first_node is None:
            self.first_node = self.last_node = DoubleLinkedListNode(
                value, None, None)
        else:
            self.first_node = DoubleLinkedListNode(
                value, None, self.first_node)
            self.first_node.next.previous = self.first_node

    def push_last(self, value):
        """
        Metoda dodaje jeden element do listy, z jej prawej strony
        """

        if self.first_node is None:
            self.first_node = self.last_node = DoubleLinkedListNode(
                value, None, None)
        else:
            self.last_node.next = DoubleLinkedListNode(
                value, self.last_node, None)
            self.last_node = self.last_node.next

    def pop_first(self):
        """
        Metoda usuwa jeden element z listy, z jej lewej strony
        """

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
        """
        Metoda usuwa jeden element z listy, z jej prawej strony
        """

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
        """
        Metoda zwraca pierwszy element listy
        """

        return self.first_node.value

    def last(self):
        """
        Metoda zwraca ostatni element listy
        """

        return self.last_node.value

    def iterator_first(self):
        """
        Metoda zwraca iterator (w tym przypadku węzeł) początku listy
        """

        return self.first_node

    def iterator_last(self):
        """
        Metoda zwraca iterator (w tym przypadku węzeł) końca listy
        """

        return self.last_node

    def empty(self):
        """
        Metoda informuje, czy lista jest pusta
        """

        return self.first_node is None

    def __iter__(self):
        """
        Metoda obsługująca iterację po liście
        """

        node = self.first_node
        while node is not None:
            yield node.value
            node = node.next

    def __reversed__(self):
        """
        Metoda obsługująca wsteczną iterację po liście
        """

        node = self.last_node
        while node is not None:
            yield node.value
            node = node.previous


    def __len__(self):
        """
        Metoda specjalna informująca o długości listy
        """

        counter = 0
        node = self.first_node
        while node is not None:
            node = node.next
            counter += 1
        return counter

    @staticmethod
    def from_list(data):
        """
        Metoda statyczna pozwalająca skonstruować listę bezpośrednio
        z tablicy
        """

        l = DoubleLinkedList()
        for element in data:
            l.push_last(element)

        return l
