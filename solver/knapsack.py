# solver/knapsack.py
import numpy as np

def solve_knapsack(values: list[float], weights: list[int], capacity: int) -> dict:
    """
    Solves the 0/1 Knapsack problem (kapnack solver) using Dynamic Programming.
    """
    n = len(values)
    dp = np.zeros((n + 1, capacity + 1))

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    # Trace back selected items
    w = capacity
    selected_indices = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_indices.append(i-1)
            w -= weights[i-1]

    return {
        "max_value": float(dp[n][capacity]),
        "selected_indices": selected_indices[::-1]
    }
