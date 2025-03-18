import numpy as np
import pandas as pd

# create a random numpy array
array= np.random.rand(3,3)

#convert it to a Pandas DataFrame
df = pd.DataFrame(array, columns=["A", "B", "C"])

# Perform an operation (calculate column-wise mean)
column_means = df.mean()

# Print results
print("Generated NumPy Array:\n", array)
print("\nConverted Pandas DataFrame:\n", df)
print("\nColumn-wise Means:\n", column_means)