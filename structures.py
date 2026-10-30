"""
Data structures module: Stack and Queue implementations with capacity limits,
event logging, and custom exception handling.
"""

from typing import Any, List, Optional, Dict
from collections import deque
import time


class StackOverflowError(Exception):
    """Raised when pushing to a stack that has reached maximum capacity."""
    pass


class StackUnderflowError(Exception):
    """Raised when popping or peeking an empty stack."""
    pass


class QueueOverflowError(Exception):
    """Raised when enqueuing to a queue that has reached maximum capacity."""
    pass


class QueueUnderflowError(Exception):
    """Raised when dequeuing or peeking an empty queue."""
    pass


class Stack:
    """
    Stack implementation based on Last-In, First-Out (LIFO).
    
    Attributes:
        capacity (int): Maximum number of elements allowed in the stack.
        items (List[Any]): Internal list holding stack elements (index 0 is bottom).
    """

    def __init__(self, capacity: int = 8):
        self.capacity = max(1, capacity)
        self.items: List[Any] = []
        self.history: List[Dict[str, Any]] = []

    def push(self, item: Any) -> Dict[str, Any]:
        """
        Pushes an element onto the top of the stack.
        Time Complexity: O(1)
        """
        if self.is_full():
            raise StackOverflowError(f"Stack overflow! Maximum capacity of {self.capacity} reached.")
        
        self.items.append(item)
        record = {
            "action": "PUSH",
            "element": item,
            "index": len(self.items) - 1,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Pushed '{item}' onto the top of the stack (index {len(self.items) - 1})."
        }
        self.history.append(record)
        return record

    def pop(self) -> Dict[str, Any]:
        """
        Removes and returns the element from the top of the stack.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise StackUnderflowError("Stack underflow! Cannot pop from an empty stack.")
        
        index = len(self.items) - 1
        item = self.items.pop()
        record = {
            "action": "POP",
            "element": item,
            "index": index,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Popped '{item}' from the top of the stack (was index {index})."
        }
        self.history.append(record)
        return record

    def peek(self) -> Dict[str, Any]:
        """
        Inspects the element at the top of the stack without removing it.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise StackUnderflowError("Stack is empty! Cannot peek.")
        
        index = len(self.items) - 1
        item = self.items[index]
        record = {
            "action": "PEEK",
            "element": item,
            "index": index,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Top element is '{item}' at index {index}."
        }
        self.history.append(record)
        return record

    def is_empty(self) -> bool:
        """Returns True if the stack has no items, False otherwise."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Returns True if the stack has reached capacity, False otherwise."""
        return len(self.items) >= self.capacity

    def size(self) -> int:
        """Returns the number of elements in the stack."""
        return len(self.items)

    def set_capacity(self, new_capacity: int) -> None:
        """Updates the maximum capacity of the stack."""
        if new_capacity < len(self.items):
            raise ValueError(f"Cannot set capacity to {new_capacity}: stack currently holds {len(self.items)} items.")
        self.capacity = max(1, new_capacity)

    def clear(self) -> Dict[str, Any]:
        """Removes all elements from the stack."""
        count = len(self.items)
        self.items.clear()
        record = {
            "action": "CLEAR",
            "element": None,
            "size": 0,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Cleared {count} items from the stack."
        }
        self.history.append(record)
        return record

    def to_dict(self) -> Dict[str, Any]:
        """Returns serialized representation of the stack state."""
        return {
            "items": list(self.items),
            "size": len(self.items),
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "top_index": len(self.items) - 1 if self.items else None,
            "top_element": self.items[-1] if self.items else None
        }


class Queue:
    """
    Queue implementation based on First-In, First-Out (FIFO).
    
    Attributes:
        capacity (int): Maximum number of elements allowed in the queue.
        items (deque): Internal double-ended queue holding elements.
                       Index 0 is the FRONT (exit), Index -1 is the REAR (entry).
    """

    def __init__(self, capacity: int = 8):
        self.capacity = max(1, capacity)
        self.items: deque = deque()
        self.history: List[Dict[str, Any]] = []

    def enqueue(self, item: Any) -> Dict[str, Any]:
        """
        Adds an element to the rear (back) of the queue.
        Time Complexity: O(1)
        """
        if self.is_full():
            raise QueueOverflowError(f"Queue overflow! Maximum capacity of {self.capacity} reached.")
        
        self.items.append(item)
        record = {
            "action": "ENQUEUE",
            "element": item,
            "index": len(self.items) - 1,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Enqueued '{item}' at the rear of the queue (index {len(self.items) - 1})."
        }
        self.history.append(record)
        return record

    def dequeue(self) -> Dict[str, Any]:
        """
        Removes and returns the element from the front of the queue.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise QueueUnderflowError("Queue underflow! Cannot dequeue from an empty queue.")
        
        item = self.items.popleft()
        record = {
            "action": "DEQUEUE",
            "element": item,
            "index": 0,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Dequeued '{item}' from the front of the queue (index 0)."
        }
        self.history.append(record)
        return record

    def peek(self) -> Dict[str, Any]:
        """
        Inspects the element at the front of the queue without removing it.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise QueueUnderflowError("Queue is empty! Cannot peek.")
        
        item = self.items[0]
        record = {
            "action": "PEEK",
            "element": item,
            "index": 0,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Front element is '{item}' at index 0."
        }
        self.history.append(record)
        return record

    def is_empty(self) -> bool:
        """Returns True if the queue has no items, False otherwise."""
        return len(self.items) == 0

    def is_full(self) -> bool:
        """Returns True if the queue has reached capacity, False otherwise."""
        return len(self.items) >= self.capacity

    def size(self) -> int:
        """Returns the number of elements in the queue."""
        return len(self.items)

    def set_capacity(self, new_capacity: int) -> None:
        """Updates the maximum capacity of the queue."""
        if new_capacity < len(self.items):
            raise ValueError(f"Cannot set capacity to {new_capacity}: queue currently holds {len(self.items)} items.")
        self.capacity = max(1, new_capacity)

    def clear(self) -> Dict[str, Any]:
        """Removes all elements from the queue."""
        count = len(self.items)
        self.items.clear()
        record = {
            "action": "CLEAR",
            "element": None,
            "size": 0,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Cleared {count} items from the queue."
        }
        self.history.append(record)
        return record

    def to_dict(self) -> Dict[str, Any]:
        """Returns serialized representation of the queue state."""
        items_list = list(self.items)
        return {
            "items": items_list,
            "size": len(items_list),
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "front_index": 0 if items_list else None,
            "front_element": items_list[0] if items_list else None,
            "rear_index": len(items_list) - 1 if items_list else None,
            "rear_element": items_list[-1] if items_list else None
        }
