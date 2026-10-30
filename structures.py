"""
Data structures module: Stack, Queue, and Sorted Linked List implementations.
Maintains internal architecture and naming in English, while providing
user-facing messages translated to Spanish per requirements.
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


class DuplicateValueError(Exception):
    """Raised when inserting a duplicate value into the sorted linked list."""
    pass


class LinkedListUnderflowError(Exception):
    """Raised when removing from an empty linked list."""
    pass


class NodeNotFoundError(Exception):
    """Raised when a specified node value is not found in the linked list."""
    pass


def normalize_value(val: Any) -> Any:
    """Helper to convert numeric strings to integer or float for proper sorting."""
    if isinstance(val, (int, float)):
        return val
    try:
        val_str = str(val).strip()
        if "." in val_str:
            return float(val_str)
        return int(val_str)
    except (ValueError, TypeError):
        return str(val).strip()


# ==========================================
# Stack (LIFO)
# ==========================================
class Stack:
    """
    Stack implementation based on Last-In, First-Out (LIFO).
    Internal code is in English; user messages are in Spanish.
    """

    def __init__(self, capacity: int = 8):
        self.capacity = max(1, capacity)
        self.items: List[Any] = []
        self.history: List[Dict[str, Any]] = []

    def push(self, item: Any) -> Dict[str, Any]:
        """Pushes an element onto the top of the stack. O(1)"""
        if self.is_full():
            raise StackOverflowError(f"¡Desbordamiento de pila (Stack Overflow)! Capacidad máxima de {self.capacity} alcanzada.")
        
        self.items.append(item)
        record = {
            "action": "PUSH",
            "element": item,
            "index": len(self.items) - 1,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Apilado '{item}' en la cima de la pila (índice {len(self.items) - 1})."
        }
        self.history.append(record)
        return record

    def pop(self) -> Dict[str, Any]:
        """Removes and returns the element from the top of the stack. O(1)"""
        if self.is_empty():
            raise StackUnderflowError("¡Subdesbordamiento de pila (Stack Underflow)! La pila está vacía.")
        
        index = len(self.items) - 1
        item = self.items.pop()
        record = {
            "action": "POP",
            "element": item,
            "index": index,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Desapilado '{item}' de la cima de la pila (estaba en índice {index})."
        }
        self.history.append(record)
        return record

    def peek(self) -> Dict[str, Any]:
        """Inspects the element at the top of the stack without removing it. O(1)"""
        if self.is_empty():
            raise StackUnderflowError("La pila está vacía. No se puede inspeccionar la cima.")
        
        index = len(self.items) - 1
        item = self.items[index]
        record = {
            "action": "PEEK",
            "element": item,
            "index": index,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Elemento en la cima es '{item}' en el índice {index}."
        }
        self.history.append(record)
        return record

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    def size(self) -> int:
        return len(self.items)

    def set_capacity(self, new_capacity: int) -> None:
        if new_capacity < len(self.items):
            raise ValueError(f"No se puede ajustar la capacidad a {new_capacity}: la pila contiene {len(self.items)} elementos.")
        self.capacity = max(1, new_capacity)

    def clear(self) -> Dict[str, Any]:
        count = len(self.items)
        self.items.clear()
        record = {
            "action": "CLEAR",
            "element": None,
            "size": 0,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Se vació la pila ({count} elementos eliminados)."
        }
        self.history.append(record)
        return record

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": list(self.items),
            "size": len(self.items),
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "top_index": len(self.items) - 1 if self.items else None,
            "top_element": self.items[-1] if self.items else None
        }


# ==========================================
# Queue (FIFO)
# ==========================================
class Queue:
    """
    Queue implementation based on First-In, First-Out (FIFO).
    Internal code is in English; user messages are in Spanish.
    """

    def __init__(self, capacity: int = 8):
        self.capacity = max(1, capacity)
        self.items: deque = deque()
        self.history: List[Dict[str, Any]] = []

    def enqueue(self, item: Any) -> Dict[str, Any]:
        """Adds an element to the rear (back) of the queue. O(1)"""
        if self.is_full():
            raise QueueOverflowError(f"¡Desbordamiento de cola (Queue Overflow)! Capacidad máxima de {self.capacity} alcanzada.")
        
        self.items.append(item)
        record = {
            "action": "ENQUEUE",
            "element": item,
            "index": len(self.items) - 1,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Encolado '{item}' al final de la cola (índice {len(self.items) - 1})."
        }
        self.history.append(record)
        return record

    def dequeue(self) -> Dict[str, Any]:
        """Removes and returns the element from the front of the queue. O(1)"""
        if self.is_empty():
            raise QueueUnderflowError("¡Subdesbordamiento de cola (Queue Underflow)! La cola está vacía.")
        
        item = self.items.popleft()
        record = {
            "action": "DEQUEUE",
            "element": item,
            "index": 0,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Desencolado '{item}' del frente de la cola (índice 0)."
        }
        self.history.append(record)
        return record

    def peek(self) -> Dict[str, Any]:
        """Inspects the element at the front of the queue without removing it. O(1)"""
        if self.is_empty():
            raise QueueUnderflowError("La cola está vacía. No se puede inspeccionar el frente.")
        
        item = self.items[0]
        record = {
            "action": "PEEK",
            "element": item,
            "index": 0,
            "size": len(self.items),
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Elemento al frente es '{item}' en el índice 0."
        }
        self.history.append(record)
        return record

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    def size(self) -> int:
        return len(self.items)

    def set_capacity(self, new_capacity: int) -> None:
        if new_capacity < len(self.items):
            raise ValueError(f"No se puede ajustar la capacidad a {new_capacity}: la cola contiene {len(self.items)} elementos.")
        self.capacity = max(1, new_capacity)

    def clear(self) -> Dict[str, Any]:
        count = len(self.items)
        self.items.clear()
        record = {
            "action": "CLEAR",
            "element": None,
            "size": 0,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Se vació la cola ({count} elementos eliminados)."
        }
        self.history.append(record)
        return record

    def to_dict(self) -> Dict[str, Any]:
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


# ==========================================
# Sorted Linked List (Lista Enlazada Ordenada)
# Reference: read.me
# - Insert: takes node and inserts in the right place (ascending, no repeated values)
# - Remove: maintains organized list (remove head, remove last node, remove specific value)
# ==========================================
class Node:
    """Node in a singly linked list."""
    def __init__(self, value: Any, next_node: Optional["Node"] = None):
        self.value = value
        self.next: Optional["Node"] = next_node

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "has_next": self.next is not None,
            "next_value": self.next.value if self.next else None
        }


class SortedLinkedList:
    """
    Singly Linked List that maintains elements in sorted ascending order
    without duplicates, adhering to classroom specifications.
    """

    def __init__(self, capacity: int = 8):
        self.head: Optional[Node] = None
        self.capacity = max(1, capacity)
        self._count = 0
        self.history: List[Dict[str, Any]] = []

    def insert(self, raw_value: Any) -> Dict[str, Any]:
        """
        Inserts a node in the correct ascending position.
        Rejects duplicates as specified in read.me.
        Time Complexity: O(N)
        """
        val = normalize_value(raw_value)

        if self.is_full():
            raise StackOverflowError(f"¡Lista llena! Capacidad máxima de {self.capacity} nodos alcanzada.")

        # Check for duplicates
        curr = self.head
        while curr is not None:
            if curr.value == val:
                raise DuplicateValueError(f"¡Valor duplicado! El valor '{val}' ya existe en la lista. No se permiten repetidos.")
            curr = curr.next

        new_node = Node(val)
        position = 0

        # Case 1: Empty list or insert before head (val < head.value)
        if self.head is None or val < self.head.value:
            new_node.next = self.head
            self.head = new_node
            position = 0
        else:
            # Case 2: Traverse to find correct spot
            prev = self.head
            position = 1
            while prev.next is not None and prev.next.value < val:
                prev = prev.next
                position += 1

            new_node.next = prev.next
            prev.next = new_node

        self._count += 1
        record = {
            "action": "INSERT",
            "element": val,
            "index": position,
            "size": self._count,
            "timestamp": time.time(),
            "time_complexity": "O(N)",
            "message": f"Insertado '{val}' en la posición {position} manteniendo orden ascendente."
        }
        self.history.append(record)
        return record

    def remove_head(self) -> Dict[str, Any]:
        """Removes the first node (head). O(1)"""
        if self.is_empty() or self.head is None:
            raise LinkedListUnderflowError("La lista está vacía. No se puede eliminar la cabeza.")

        removed_val = self.head.value
        self.head = self.head.next
        self._count -= 1

        record = {
            "action": "REMOVE_HEAD",
            "element": removed_val,
            "index": 0,
            "size": self._count,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Eliminada la cabeza con valor '{removed_val}'. La lista permanece organizada."
        }
        self.history.append(record)
        return record

    def remove_tail(self) -> Dict[str, Any]:
        """Removes the last node in the list. O(N)"""
        if self.is_empty() or self.head is None:
            raise LinkedListUnderflowError("La lista está vacía. No se puede eliminar el último nodo.")

        # Single element
        if self.head.next is None:
            removed_val = self.head.value
            self.head = None
            self._count = 0
            record = {
                "action": "REMOVE_TAIL",
                "element": removed_val,
                "index": 0,
                "size": 0,
                "timestamp": time.time(),
                "time_complexity": "O(1)",
                "message": f"Eliminado el último nodo (cabeza única) con valor '{removed_val}'."
            }
            self.history.append(record)
            return record

        # Traverse to node right before the tail
        prev = self.head
        idx = 1
        while prev.next is not None and prev.next.next is not None:
            prev = prev.next
            idx += 1

        removed_val = prev.next.value
        prev.next = None
        self._count -= 1

        record = {
            "action": "REMOVE_TAIL",
            "element": removed_val,
            "index": idx,
            "size": self._count,
            "timestamp": time.time(),
            "time_complexity": "O(N)",
            "message": f"Eliminado el último nodo con valor '{removed_val}'. La lista permanece organizada."
        }
        self.history.append(record)
        return record

    def remove_value(self, raw_value: Any) -> Dict[str, Any]:
        """Searches and removes a specific node by value. O(N)"""
        if self.is_empty() or self.head is None:
            raise LinkedListUnderflowError("La lista está vacía. No se puede eliminar ningún nodo.")

        val = normalize_value(raw_value)

        # If it's the head node
        if self.head.value == val:
            return self.remove_head()

        prev = self.head
        idx = 1
        while prev.next is not None and prev.next.value != val:
            prev = prev.next
            idx += 1

        if prev.next is None:
            raise NodeNotFoundError(f"El nodo con valor '{val}' no existe en la lista.")

        removed_val = prev.next.value
        prev.next = prev.next.next
        self._count -= 1

        record = {
            "action": "REMOVE_VAL",
            "element": removed_val,
            "index": idx,
            "size": self._count,
            "timestamp": time.time(),
            "time_complexity": "O(N)",
            "message": f"Eliminado el nodo '{removed_val}' en la posición {idx}. La lista permanece organizada."
        }
        self.history.append(record)
        return record

    def search(self, raw_value: Any) -> Dict[str, Any]:
        """Searches for a value and returns its position and comparisons count. O(N)"""
        if self.is_empty():
            raise LinkedListUnderflowError("La lista está vacía. No hay elementos para buscar.")

        val = normalize_value(raw_value)
        curr = self.head
        idx = 0
        comparisons = 0

        while curr is not None:
            comparisons += 1
            if curr.value == val:
                record = {
                    "action": "SEARCH",
                    "element": val,
                    "index": idx,
                    "comparisons": comparisons,
                    "found": True,
                    "timestamp": time.time(),
                    "time_complexity": "O(N)",
                    "message": f"Encontrado '{val}' en la posición {idx} tras {comparisons} comparaciones."
                }
                self.history.append(record)
                return record
            curr = curr.next
            idx += 1

        raise NodeNotFoundError(f"El valor '{val}' no fue encontrado en la lista (revisadas {comparisons} posiciones).")

    def is_empty(self) -> bool:
        return self._count == 0

    def is_full(self) -> bool:
        return self._count >= self.capacity

    def size(self) -> int:
        return self._count

    def set_capacity(self, new_capacity: int) -> None:
        if new_capacity < self._count:
            raise ValueError(f"No se puede ajustar la capacidad a {new_capacity}: la lista contiene {self._count} nodos.")
        self.capacity = max(1, new_capacity)

    def clear(self) -> Dict[str, Any]:
        count = self._count
        self.head = None
        self._count = 0
        record = {
            "action": "CLEAR",
            "element": None,
            "size": 0,
            "timestamp": time.time(),
            "time_complexity": "O(1)",
            "message": f"Se vació la lista enlazada ({count} nodos eliminados)."
        }
        self.history.append(record)
        return record

    def to_list(self) -> List[Any]:
        items = []
        curr = self.head
        while curr is not None:
            items.append(curr.value)
            curr = curr.next
        return items

    def to_dict(self) -> Dict[str, Any]:
        nodes_list = []
        curr = self.head
        idx = 0
        while curr is not None:
            nodes_list.append({
                "index": idx,
                "value": curr.value,
                "next_value": curr.next.value if curr.next else None,
                "is_head": idx == 0,
                "is_tail": curr.next is None
            })
            curr = curr.next
            idx += 1

        items = [n["value"] for n in nodes_list]
        return {
            "items": items,
            "nodes": nodes_list,
            "size": self._count,
            "capacity": self.capacity,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "head": items[0] if items else None,
            "tail": items[-1] if items else None
        }
