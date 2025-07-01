
# Simple stack data structure for managing game states
from dataclasses import dataclass

@dataclass
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        """Return True if the stack is empty."""
        return self.items == []

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Pop the top item from the stack."""
        return self.items.pop()

    def peek(self):
        """Return the top item without removing it."""
        return self.items[len(self.items) - 1]

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)
