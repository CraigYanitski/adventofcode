import numpy as np
import pandas as pd

# Part I
# find total distance between ordered lists
test_data_l = np.array([3, 4, 2, 1, 3, 3])
test_data_r = np.array([4, 3, 5, 9, 3, 3])
data = pd.read_csv("input_1", names=["left", "right"], sep="\s+")
list_l = np.sort(data.left.to_numpy())
list_r = np.sort(data.right.to_numpy())
list_diff = np.abs(list_l - list_r)

print(list_diff.sum())

# Part II
# find number of occurrences of numbers in the left list in the right list
list_sim = np.array([_ * np.ones_like(
    np.where(list_r == _)[0]).sum() for _ in list_l])
print(list_sim.sum())
