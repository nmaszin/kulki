from app.list import DoubleLinkedList
from unittest import TestCase

class TestDoubleLinkedList(TestCase):
    def test_push_last_one_element(self):
        l = DoubleLinkedList()
        l.push_last(1)

        self.assertEqual(list(l), [1])

    def test_push_last_a_few_elements(self):
        l = DoubleLinkedList()
        l.push_last(1)
        l.push_last(2)
        l.push_last(3)

        self.assertEqual(list(l), [1, 2, 3])
    
    def test_push_first_one_element(self):
        l = DoubleLinkedList()
        l.push_first(1)

        self.assertEqual(list(l), [1])

    def test_push_first_a_few_elements(self):
        l = DoubleLinkedList()
        l.push_first(1)
        l.push_first(2)
        l.push_first(3)

        self.assertEqual(list(l), [3, 2, 1])

    def test_creating_list_from_static_method(self):
        l = DoubleLinkedList.from_list([1, 2, 3, 4, 5])

        self.assertEqual(list(l), [1, 2, 3, 4, 5])

    def test_pop_last_one_element(self):
        l = DoubleLinkedList().from_list([1, 2, 3, 4, 5])
        l.pop_last()

        self.assertEqual(list(l), [1, 2, 3, 4])
    
    def test_pop_last_few_elements(self):
        l = DoubleLinkedList().from_list([1, 2, 3, 4, 5])
        l.pop_last()
        l.pop_last()
        l.pop_last()

        self.assertEqual(list(l), [1, 2])

    def test_pop_first_one_element(self):
        l = DoubleLinkedList().from_list([1, 2, 3, 4, 5])
        l.pop_first()

        self.assertEqual(list(l), [2, 3, 4, 5])
    
    def test_pop_first_few_elements(self):
        l = DoubleLinkedList().from_list([1, 2, 3, 4, 5])
        l.pop_first()
        l.pop_first()
        l.pop_first()

        self.assertEqual(list(l), [4, 5])

    def test_reverse(self):
        l = DoubleLinkedList.from_list([1, 2, 3, 4, 5])
        
        self.assertEqual(list(reversed(l)), [5, 4, 3, 2, 1])
    
    def test_non_empty(self):
        l = DoubleLinkedList.from_list([1, 2, 3, 4, 5])

        self.assertFalse(l.empty())
    
    def test_empty(self):
        l = DoubleLinkedList()

        self.assertTrue(l.empty())
    
    def test_0_len(self):
        l = DoubleLinkedList()

        self.assertEqual(len(l), 0)
    
    def test_5_len(self):
        l = DoubleLinkedList.from_list([1, 2, 3, 4, 5])

        self.assertEqual(len(l), 5)

    def test_iterate_with_iterator(self):
        l = DoubleLinkedList.from_list([1, 2, 3, 4, 5])

        accumulator = []
        it = l.iterator_first()
        while it is not None:
            accumulator.append(it.value)
            it = it.next

        self.assertEqual(accumulator, [1, 2, 3, 4, 5])
        
