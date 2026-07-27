import heapq
from collections import deque

# ============================================
# Exercise 1: Binary Search Tree (BST)
# ============================================
print("=" * 60)
print("Exercise 1: Binary Search Tree")
print("=" * 60)

class Node:
    """Node for Binary Search Tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    """
    Insert a value into BST
    Returns the root of the tree
    """
    if root is None:
        return Node(value)
    
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    # If equal, we don't insert duplicates
    
    return root

def inorder_traversal(root):
    """
    In-order traversal: Left -> Root -> Right
    This gives values in sorted order
    """
    if root is None:
        return []
    
    result = []
    result.extend(inorder_traversal(root.left))
    result.append(root.value)
    result.extend(inorder_traversal(root.right))
    return result

def print_tree(root, level=0, prefix="Root: "):
    """Print tree structure (visual)"""
    if root is None:
        return
    
    print("  " * level + prefix + str(root.value))
    if root.left or root.right:
        print_tree(root.left, level + 1, "L--- ")
        print_tree(root.right, level + 1, "R--- ")

# Test BST
balances = [50, 30, 70, 20, 40, 60, 80, 25, 35]
print(f"Inserting balances: {balances}")

# Build BST
bst_root = None
for balance in balances:
    bst_root = insert(bst_root, balance)

print("\nBST Structure:")
print_tree(bst_root)

print("\nIn-order Traversal (sorted):")
sorted_values = inorder_traversal(bst_root)
print(sorted_values)
print(f"✓ BST in-order gives sorted order: {sorted_values == sorted(balances)}")
print()

# ============================================
# Exercise 2: Tree Height (Depth)
# ============================================
print("=" * 60)
print("Exercise 2: Tree Height")
print("=" * 60)

def height(node):
    """
    Calculate height of binary tree
    Height = number of edges on longest path from root to leaf
    Empty tree has height -1 (or 0 depending on definition)
    """
    if node is None:
        return -1  # Empty tree
    
    # Recursively get height of left and right subtrees
    left_height = height(node.left)
    right_height = height(node.right)
    
    # Height is max of left/right + 1 for current node
    return max(left_height, right_height) + 1

def depth(node):
    """
    Alternative: depth (number of nodes on longest path)
    Empty tree has depth 0
    """
    if node is None:
        return 0
    return max(depth(node.left), depth(node.right)) + 1

# Test height function
print(f"BST Root: {bst_root.value}")
print(f"Height (edges): {height(bst_root)}")
print(f"Depth (nodes): {depth(bst_root)}")

# Test on different trees
print("\nTesting on different trees:")
single_node = Node(10)
print(f"Single node - Height: {height(single_node)}, Depth: {depth(single_node)}")

# Create unbalanced tree
unbalanced = Node(1)
unbalanced.right = Node(2)
unbalanced.right.right = Node(3)
unbalanced.right.right.right = Node(4)
print(f"Unbalanced tree - Height: {height(unbalanced)}, Depth: {depth(unbalanced)}")

# Empty tree
print(f"Empty tree - Height: {height(None)}, Depth: {depth(None)}")
print()

# ============================================
# Exercise 3: Graph BFS
# ============================================
print("=" * 60)
print("Exercise 3: Graph BFS (Breadth-First Search)")
print("=" * 60)

def bfs(graph, start):
    """
    BFS traversal of graph using queue
    Returns set of reachable vertices
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(f"  Visiting: {vertex}")
        
        # Visit all neighbors
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited

# Create a graph (adjacency list)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("Graph (adjacency list):")
for node, neighbors in graph.items():
    print(f"  {node} -> {neighbors}")

print("\nBFS starting from 'A':")
reachable = bfs(graph, 'A')
print(f"\nReachable vertices: {sorted(reachable)}")

print("\nBFS starting from 'D':")
reachable = bfs(graph, 'D')
print(f"\nReachable vertices: {sorted(reachable)}")
print()

# ============================================
# Exercise 4: Graph DFS (Recursive)
# ============================================
print("=" * 60)
print("Exercise 4: Graph DFS (Depth-First Search)")
print("=" * 60)

def dfs(graph, start, visited=None):
    """
    DFS traversal using recursion
    Returns set of reachable vertices
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(f"  Visiting: {start}")
    
    # Visit all neighbors
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited

print("DFS starting from 'A':")
reachable_dfs = dfs(graph, 'A')
print(f"\nReachable vertices: {sorted(reachable_dfs)}")

print("\nDFS starting from 'D':")
reachable_dfs = dfs(graph, 'D')
print(f"\nReachable vertices: {sorted(reachable_dfs)}")

# Compare BFS and DFS order
print("\nBFS vs DFS Visit Order:")
print("BFS from 'A':")
bfs(graph, 'A')
print("\nDFS from 'A':")
dfs(graph, 'A')

print("\nKey difference:")
print("  • BFS: Explores neighbors first (level by level)")
print("  • DFS: Explores deep paths first (branch by branch)")
print()

# ============================================
# Exercise 5: Priority Queue with heapq
# ============================================
print("=" * 60)
print("Exercise 5: Priority Queue (heapq)")
print("=" * 60)

def demonstrate_priority_queue():
    """
    Use heapq to implement priority queue
    """
    # Create empty heap
    priority_queue = []
    
    # Tasks with priorities (lower number = higher priority)
    tasks = [
        (3, "Check emails"),
        (1, "Emergency: Server down!"),
        (4, "Schedule meeting"),
        (2, "Review code"),
        (5, "Clean desk")
    ]
    
    print("Tasks with priorities (lower number = higher priority):")
    for priority, task in tasks:
        print(f"  Priority {priority}: {task}")
    
    print("\nPushing tasks onto heap:")
    for priority, task in tasks:
        heapq.heappush(priority_queue, (priority, task))
        print(f"  Pushed: ({priority}, {task})")
        print(f"  Heap size: {len(priority_queue)}")
    
    print("\nPopping tasks (should come out by priority):")
    print("-" * 40)
    while priority_queue:
        priority, task = heapq.heappop(priority_queue)
        print(f"  Priority {priority}: {task}")
        print(f"  Remaining: {len(priority_queue)}")
    
    print("\n✓ Tasks popped in priority order (1 = highest priority)")

demonstrate_priority_queue()

# ============================================
# Additional Example: Priority Queue with objects
# ============================================
print("\n" + "=" * 60)
print("Bonus: Priority Queue with Account Balances")
print("=" * 60)

def priority_demo_with_accounts():
    """Use priority queue to process accounts by balance"""
    
    # Accounts with balances
    accounts = [
        (1500, "Alem Tesfaye"),
        (800, "Bekele Hailu"),
        (2000, "Chaltu Abebe"),
        (3000, "Eden Girma"),
        (500, "Fikir Tadesse")
    ]
    
    # Create priority queue (highest balance = highest priority)
    pq = []
    for balance, name in accounts:
        # Use negative balance for max-heap behavior
        heapq.heappush(pq, (-balance, name))
    
    print("Processing accounts by highest balance first:")
    print("-" * 40)
    while pq:
        neg_balance, name = heapq.heappop(pq)
        balance = -neg_balance
        print(f"  {name:20s} {balance:8.2f} ETB")
        print(f"  Remaining accounts: {len(pq)}")

priority_demo_with_accounts()

# ============================================
# Summary
# ============================================
print("\n" + "=" * 60)
print("SUMMARY - Data Structures")
print("=" * 60)

print("\n1. Binary Search Tree:")
print("   - Insert: O(log n) average")
print("   - In-order traversal: O(n), gives sorted order")
print("   - Height calculation: O(n)")

print("\n2. Graph Traversal:")
print("   - BFS: O(V + E) using queue")
print("   - DFS: O(V + E) using recursion")
print("   - BFS finds shortest path, DFS goes deep")

print("\n3. Priority Queue (heapq):")
print("   - Push: O(log n)")
print("   - Pop: O(log n)")
print("   - Always returns smallest priority first")

print("\n" + "=" * 60)
print("All exercises completed successfully!")
print("=" * 60)
