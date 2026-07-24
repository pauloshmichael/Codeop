import random

# ============================================
# Exercise 1: Recursion
# ============================================
print("=" * 50)
print("Exercise 1: Recursion")
print("=" * 50)

def recursive_sum(nums):
    """
    Recursively sum a list of numbers
    Base case: empty list returns 0
    Recursive case: first element + sum of rest
    """
    if not nums:  # Base case
        return 0
    return nums[0] + recursive_sum(nums[1:])  # Recursive case

def count_down(n):
    """
    Recursively count down from n to 1
    Base case: n <= 0, just print
    Recursive case: print n, then count down from n-1
    """
    if n <= 0:
        return
    print(n, end=" ")
    count_down(n - 1)

# Test recursive functions
numbers = [1, 2, 3, 4, 5]
print(f"List: {numbers}")
print(f"Sum using recursion: {recursive_sum(numbers)}")
print(f"Sum using built-in: {sum(numbers)}")

print("\nCountdown from 5:")
count_down(5)
print()  # New line
print()

# ============================================
# Exercise 2: Binary Search
# ============================================
print("=" * 50)
print("Exercise 2: Binary Search")
print("=" * 50)

def binary_search(items, target):
    """
    Binary search on sorted list
    Returns index of target or -1 if not found
    O(log n) - divides search space in half each step
    """
    left = 0
    right = len(items) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half
    
    return -1  # Not found

# Test binary search
balances = [100, 250, 300, 450, 500, 750, 1000, 1200]
print(f"Sorted balances: {balances}")

# Test finding existing values
for target in [300, 750, 1000]:
    index = binary_search(balances, target)
    print(f"Found {target} at index {index}")

# Test finding non-existing value
target = 600
index = binary_search(balances, target)
print(f"Found {target} at index {index} (not found, returns -1)")
print()

# ============================================
# Exercise 3: Merge Sort
# ============================================
print("=" * 50)
print("Exercise 3: Merge Sort")
print("=" * 50)

def merge_sort(items):
    """
    Merge sort - O(n log n)
    Divides list in half, sorts each half, then merges
    """
    # Base case: list of 0 or 1 element is already sorted
    if len(items) <= 1:
        return items
    
    # Divide
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    
    # Conquer (merge)
    return merge(left, right)

def merge(left, right):
    """
    Merge two sorted lists into one sorted list
    """
    result = []
    i = j = 0
    
    # Compare elements from left and right
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# Test merge sort
random.seed(42)  # For reproducible results
test_list = [random.randint(1, 100) for _ in range(10)]
print(f"Original list: {test_list}")

sorted_merge = merge_sort(test_list)
print(f"Merge sorted: {sorted_merge}")

sorted_builtin = sorted(test_list)
print(f"Built-in sort: {sorted_builtin}")

print(f"Sort matches built-in? {sorted_merge == sorted_builtin}")

# Test on multiple random lists
print("\nTesting on 5 random lists:")
for i in range(5):
    random_list = [random.randint(1, 50) for _ in range(7)]
    merge_result = merge_sort(random_list)
    builtin_result = sorted(random_list)
    match = merge_result == builtin_result
    print(f"  List {i+1}: {'✓' if match else '✗'} matches built-in sort")
print()

# ============================================
# Exercise 4: Sort with Key
# ============================================
print("=" * 50)
print("Exercise 4: Sort with Key")
print("=" * 50)

# List of (name, balance) tuples
accounts = [
    ("Alem Tesfaye", 1500),
    ("Bekele Hailu", 800),
    ("Chaltu Abebe", 2000),
    ("Dawit Mengistu", 1200),
    ("Eden Girma", 3000),
]

print("Original list (name, balance):")
for name, balance in accounts:
    print(f"  {name}: {balance} ETB")

# Sort by balance descending (highest first)
sorted_by_balance = sorted(accounts, key=lambda x: x[1], reverse=True)

print("\nSorted by balance descending:")
for name, balance in sorted_by_balance:
    print(f"  {name}: {balance} ETB")

# Sort by name alphabetically
sorted_by_name = sorted(accounts, key=lambda x: x[0])

print("\nSorted by name alphabetically:")
for name, balance in sorted_by_name:
    print(f"  {name}: {balance} ETB")

# Sort by balance ascending (lowest first)
sorted_by_balance_asc = sorted(accounts, key=lambda x: x[1])

print("\nSorted by balance ascending:")
for name, balance in sorted_by_balance_asc:
    print(f"  {name}: {balance} ETB")
print()

# ============================================
# Exercise 5: Two Pointers
# ============================================
print("=" * 50)
print("Exercise 5: Two Pointers - Find Pair Sum")
print("=" * 50)

def has_pair(nums, target):
    """
    Check if any two numbers in sorted list sum to target
    Uses two pointers: left and right
    O(n) time complexity
    """
    left = 0
    right = len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            print(f"  Found: {nums[left]} + {nums[right]} = {target}")
            return True
        elif current_sum < target:
            left += 1  # Need bigger sum, move left pointer right
        else:
            right -= 1  # Need smaller sum, move right pointer left
    
    print(f"  No pair found that sums to {target}")
    return False

# Test two pointers
numbers = [1, 3, 5, 7, 9, 11, 13, 15]
print(f"Sorted numbers: {numbers}")

print("\nSearching for pairs that sum to 16:")
has_pair(numbers, 16)  # 3 + 13 = 16, 5 + 11 = 16, 7 + 9 = 16

print("\nSearching for pairs that sum to 20:")
has_pair(numbers, 20)  # 7 + 13 = 20, 9 + 11 = 20

print("\nSearching for pairs that sum to 10:")
has_pair(numbers, 10)  # 1 + 9 = 10, 3 + 7 = 10

print("\nSearching for pairs that sum to 25:")
has_pair(numbers, 25)  # 10 + 15 = 25 (but 10 isn't in list)

print("\nSearching for pairs that sum to 14:")
has_pair(numbers, 14)  # 1 + 13 = 14, 3 + 11 = 14

# Test on balances
balances = [100, 250, 300, 450, 500, 750, 1000, 1200]
print(f"\nBalances: {balances}")
print("Searching for pairs that sum to 1000:")
has_pair(balances, 1000)  # 250 + 750 = 1000

# ============================================
# Bonus: Visual Comparison of Sorting Algorithms
# ============================================
print("\n" + "=" * 50)
print("Bonus: Algorithm Comparison")
print("=" * 50)

def bubble_sort(items):
    """Simple bubble sort - O(n²)"""
    arr = items.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Compare algorithms
test_data = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {test_data}")
print(f"Bubble sort: {bubble_sort(test_data)}")
print(f"Merge sort: {merge_sort(test_data)}")
print(f"Built-in sort: {sorted(test_data)}")

print("\nAll sorting algorithms produce the same result!")
print()

# ============================================
# Summary
# ============================================
print("=" * 50)
print("SUMMARY - Time Complexities")
print("=" * 50)

print("\n1. Recursive Sum: O(n)")
print("   - Makes n recursive calls, one for each element")

print("\n2. Binary Search: O(log n)")
print("   - Divides search space in half each step")

print("\n3. Merge Sort: O(n log n)")
print("   - Divides (log n) and merges (n)")

print("\n4. Sort with Key: O(n log n)")
print("   - Built-in sorting with custom key")

print("\n5. Two Pointers: O(n)")
print("   - Single pass through the list")

print("\n" + "=" * 50)
print("All exercises completed successfully!")
print("=" * 50)
