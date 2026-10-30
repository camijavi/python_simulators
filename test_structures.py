"""
Unit tests for Stack and Queue data structures.
"""

import unittest
from structures import (
    Stack,
    Queue,
    StackOverflowError,
    StackUnderflowError,
    QueueOverflowError,
    QueueUnderflowError,
)


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack(capacity=4)

    def test_initial_state(self):
        self.assertTrue(self.stack.is_empty())
        self.assertFalse(self.stack.is_full())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(self.stack.to_dict()["items"], [])

    def test_push_and_peek(self):
        rec1 = self.stack.push("Alpha")
        self.assertEqual(rec1["action"], "PUSH")
        self.assertEqual(rec1["element"], "Alpha")
        self.assertEqual(self.stack.size(), 1)
        self.assertFalse(self.stack.is_empty())

        peek_rec = self.stack.peek()
        self.assertEqual(peek_rec["element"], "Alpha")
        self.assertEqual(self.stack.size(), 1)

        self.stack.push("Beta")
        self.assertEqual(self.stack.peek()["element"], "Beta")
        self.assertEqual(self.stack.size(), 2)

    def test_pop_lifo_order(self):
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)

        # LIFO: 30 should come off first, then 20, then 10
        pop1 = self.stack.pop()
        self.assertEqual(pop1["element"], 30)

        pop2 = self.stack.pop()
        self.assertEqual(pop2["element"], 20)

        pop3 = self.stack.pop()
        self.assertEqual(pop3["element"], 10)

        self.assertTrue(self.stack.is_empty())

    def test_stack_overflow(self):
        for i in range(4):
            self.stack.push(f"Item {i}")
        self.assertTrue(self.stack.is_full())

        with self.assertRaises(StackOverflowError):
            self.stack.push("Item 5")

    def test_stack_underflow(self):
        with self.assertRaises(StackUnderflowError):
            self.stack.pop()

        with self.assertRaises(StackUnderflowError):
            self.stack.peek()

    def test_clear(self):
        self.stack.push(1)
        self.stack.push(2)
        rec = self.stack.clear()
        self.assertEqual(rec["action"], "CLEAR")
        self.assertTrue(self.stack.is_empty())


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue(capacity=4)

    def test_initial_state(self):
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue.is_full())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(self.queue.to_dict()["items"], [])

    def test_enqueue_and_peek(self):
        rec1 = self.queue.enqueue("Patient 1")
        self.assertEqual(rec1["action"], "ENQUEUE")
        self.assertEqual(rec1["element"], "Patient 1")
        self.assertEqual(self.queue.size(), 1)

        peek_rec = self.queue.peek()
        self.assertEqual(peek_rec["element"], "Patient 1")

        self.queue.enqueue("Patient 2")
        # Peek should still show the front item: Patient 1
        self.assertEqual(self.queue.peek()["element"], "Patient 1")
        self.assertEqual(self.queue.size(), 2)

    def test_dequeue_fifo_order(self):
        self.queue.enqueue("A")
        self.queue.enqueue("B")
        self.queue.enqueue("C")

        # FIFO: A should come off first, then B, then C
        deq1 = self.queue.dequeue()
        self.assertEqual(deq1["element"], "A")

        deq2 = self.queue.dequeue()
        self.assertEqual(deq2["element"], "B")

        deq3 = self.queue.dequeue()
        self.assertEqual(deq3["element"], "C")

        self.assertTrue(self.queue.is_empty())

    def test_queue_overflow(self):
        for i in range(4):
            self.queue.enqueue(i)
        self.assertTrue(self.queue.is_full())

        with self.assertRaises(QueueOverflowError):
            self.queue.enqueue(99)

    def test_queue_underflow(self):
        with self.assertRaises(QueueUnderflowError):
            self.queue.dequeue()

        with self.assertRaises(QueueUnderflowError):
            self.queue.peek()

    def test_clear(self):
        self.queue.enqueue("Job 1")
        self.queue.enqueue("Job 2")
        rec = self.queue.clear()
        self.assertEqual(rec["action"], "CLEAR")
        self.assertTrue(self.queue.is_empty())


if __name__ == "__main__":
    unittest.main()
