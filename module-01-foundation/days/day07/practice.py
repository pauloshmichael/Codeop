import time
from collections import deque

# ============================================
# Exercise 1: Big-O Notation Analysis
# ============================================
print("=" * 50)
print("Exercise 1: Big-O Notation")
print("=" * 50)

# 1. List Index - O(1)
numbers = [1, 2, 3, 4, 5]
x = numbers[2]  # O(1)
print("1. List index: O(1) - Direct access")

# 2. Single Loop - O(n)
n = 10
for i in range(n):  # O(n)
    pass
print("2. Single loop: O(n) - Linear growth")

# 3. Nested Loop - O(n²)
for i in range(n):      # O(n)
    for j in range(n):  # O(n) - runs n times per outer loop
        pass
print("3. Nested loop: O(n²) - Quadratic growth")

# 4. Dict Lookup - O(1)
d = {'key': 'value'}
y = d['key']  # O(1)
print("4. Dict lookup: O(1) - Hash table access")

# 5. Binary Search - O(log n)
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
left, right = 0, len(arr) - 1
target = 7
while left <= right:  # O(log n) - halves search space each time
    mid = (left + right) // 2
    if arr[mid] == target:
        break
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
print("5. Binary search: O(log n) - Divides in half each step")
print()

# ============================================
# Exercise 2: List vs Dict Lookup
# ============================================
print("=" * 50)
print("Exercise 2: List vs Dict Lookup")
print("=" * 50)

# Create 100,000 fake account numbers
size = 100000
accounts = list(range(size))

# Create list and dict
acc_list = accounts[:]
acc_dict = {num: True for num in accounts}

# Find a number near the end
target = accounts[-1]

# List lookup
print(f"\nLooking for {target} in list...")
start = time.time()
found_in_list = target in acc_list
list_time = time.time() - start
print(f"List lookup: {list_time:.6f} seconds")

# Dict lookup
print(f"Looking for {target} in dict...")
start = time.time()
found_in_dict = target in acc_dict
dict_time = time.time() - start
print(f"Dict lookup: {dict_time:.6f} seconds")

print(f"\nDict is {list_time/dict_time:.2f}x faster!")
print("List: O(n) - searches through all elements")
print("Dict: O(1) - direct hash lookup")
print()

# ============================================
# Exercise 3: Stack Implementation
# ============================================
print("=" * 50)
print("Exercise 3: Stack - Reverse Names")
print("=" * 50)

class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

# Use stack to reverse names
names = ["Alem", "Bekele", "Chaltu", "Dawit", "Eden"]
print(f"Original: {names}")

# Push all names onto stack
stack = Stack()
for name in names:
    stack.push(name)

# Pop to reverse
reversed_names = []
while not stack.is_empty():
    reversed_names.append(stack.pop())

print(f"Reversed: {reversed_names}")
print()

# ============================================
# Exercise 4: Queue with deque
# ============================================
print("=" * 50)
print("Exercise 4: Bank Queue")
print("=" * 50)

# Create a queue
queue = deque()

# Enqueue customers
customers = ["Alem", "Bekele", "Chaltu", "Dawit", "Eden"]
print("Customers joining the line:")
for customer in customers:
    queue.append(customer)
    print(f"  {customer} joined")

# Serve customers (FIFO)
print("\nServing customers:")
counter = 1
while queue:
    customer = queue.popleft()
    print(f"  {counter}. Serving: {customer}")
    counter += 1

print("All customers served!")
print()

# ============================================
# Exercise 5: Singly Linked List
# ============================================
print("=" * 50)
print("Exercise 5: Singly Linked List")
print("=" * 50)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def push_front(self, data):
        """Add node to the front"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def print_all(self):
        """Print all nodes by walking the chain"""
        if not self.head:
            print("Empty list")
            return
        
        current = self.head
        position = 1
        while current:
            print(f"  Position {position}: {current.data}")
            current = current.next
            position += 1

# Create linked list
ll = LinkedList()
print("Pushing items to front:")
ll.push_front("Eden")
ll.push_front("Dawit")
ll.push_front("Chaltu")
ll.push_front("Bekele")
ll.push_front("Alem")

print("\nLinked List contents (walking the chain):")
ll.print_all()

# Show the chain structure
print("\nChain structure (showing next pointers):")
current = ll.head
while current:
    next_data = current.next.data if current.next else "None"
    print(f"  {current.data} -> {next_data}")
    current = current.next

print("\nAll exercises completed!")