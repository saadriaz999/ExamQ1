"""
This script compares two dynamic programming approaches to solve a string partitioning problem, where the goal is 
to minimize the cost of splitting a string into substrings. The my_approach uses a 2D DP table and evaluates all 
possible splits, resulting in a O(n^3) time complexity, while the optimal_approach uses a 1D DP array and reduces 
complexity to O(n^2). The script tests both approaches with different black-box cost functions across various test cases.
"""

def my_approach(y, B):
    """
    Solve the problem using your exact approach with the given black-box function.

    :param y: Input string
    :param B: A black-box function to compute cost for substrings
    :return: Minimum cost
    """
    # Length of the string
    n = len(y)

    # Create a DP table for storing the minimum cost
    dp = [[float('inf') for _ in range(n)] for _ in range(n)]

    # Initialize base case: single characters
    for i in range(n):
        dp[i][i] = B(y[i])

    # Fill the DP table for substrings of increasing lengths
    for l in range(1, n + 1):  # Length of the substring
        for i in range(n - l):  # Start index of the substring
            j = i + l  # End index of the substring

            # Option 1: Treat the entire substring as a single block
            dp[i][j] = B(y[i:j + 1])

            # Option 2: Split the substring into two parts and find the minimum cost
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])

    # Return the minimum cost for the entire string
    return dp[0][n - 1]

def optimal_approach(y, B):
    """
    Solve the problem using an optimized approach with the given black-box function.

    :param y: Input string
    :param B: A black-box function to compute cost for substrings
    :return: Minimum cost
    """
    n = len(y)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for j in range(i):
            dp[i] = min(dp[i], dp[j] + B(y[j:i]))

    return dp[n]

# Black-box function 1 (original):
def B1(s):
    return sum(ord(c) - ord('a') + 1 for c in s)

# Black-box function 2: Penalize substrings with unique characters
def B2(s):
    unique_chars = len(set(s))
    return sum(ord(c) - ord('a') + 1 for c in s) + unique_chars**2

# Black-box function 3: Bonus for repeated characters
def B3(s):
    char_count = {c: s.count(c) for c in set(s)}
    bonus = sum(count**2 for count in char_count.values())
    return len(s)**2 + bonus

# Black-box function 4: Penalize substrings based on length
def B4(s):
    return len(s)**3 + sum(ord(c) - ord('a') + 1 for c in s)

# Black-box function 5: Penalize based on alternating characters
def B5(s):
    penalty = sum(1 for i in range(1, len(s)) if s[i] != s[i - 1])
    return len(s) + penalty * 5

# Black-box function 6: Complexity based on vowel count
def B6(s):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    vowel_count = sum(1 for c in s if c in vowels)
    return sum(ord(c) - ord('a') + 1 for c in s) + vowel_count * 10

# Test cases
test_cases = ["cat", "aaaa", "ababab", "fjasdlfdfasd", "ajksldjfasdfjaskldfjas"]
black_box_functions = [B1, B2, B3, B4, B5, B6]

print("Testing Both Approaches with Different Black-Box Functions:")
results = []
for idx, B in enumerate(black_box_functions, 1):
    print(f"\nUsing Black-Box Function B{idx}:")
    for test in test_cases:
        my_result = my_approach(test, B)
        optimal_result = optimal_approach(test, B)
        results.append((f"B{idx}", test, my_result, optimal_result))
        print(f"String: {test} -> My Approach: {my_result}, Optimal Approach: {optimal_result}")
