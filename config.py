from collections import OrderedDict

C = [[0, 0, 0, 1, 0],
     [0, 0, 1, 0, 1],
     [0, 1, 0, 0, 0],
     [0, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 1, 1, 0],
     [1, 1, 0, 1, 1],
     [1, 1, 1, 0, 0],]
CFeatures = ["A", "B", "C", "D"]


C = [[1, 1, 1],
     [1, 0, 0],
     [0, 1, 0],
     [0, 0, 0],]
CFeatures = ["Fur", "Barks"]

C = [[1, 0, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 1, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [1, 0, 1, 0, 1],
     [0, 0, 0, 0, 1],
     [0, 0, 1, 0, 1],
     [0, 1, 0, 0, 1],
     [0, 1, 1, 0, 1],]
CFeatures = ["A", "B", "C", "D"]

C = [
    [2, 10, 1],  # Example 1: Large size and heavy weight => Heavy
    [2, 5, 0],   # Example 2: Large size but moderate weight => Not Heavy
    [1, 8, 1],   # Example 3: Small size but heavy weight => Heavy
    [1, 3, 0],   # Example 4: Small size and light weight => Not Heavy
    [3, 15, 1],  # Example 5: Very large size and very heavy weight => Heavy
    [3, 6, 1],   # Example 6: Very large size but moderate weight => Not Heavy
    [2, 6, 0],
]
CFeatures = ["Size", "Weight"]

C = [
    [5, 8, 7, 10, 1],
    [3, 6, 2, 9, 0],
    [6, 9, 5, 12, 1],
    [2, 4, 8, 8, "red"],
    [7, 7, 6, 11, 1],    
    [4, 5, 3, 7, 0],
    [8, 10, 4, 13, 1],
    [1, 3, 9, 6, 2]
]
CFeatures = ["A", "B", "C", "D"]

C = [[0, 0, 0, 1, 0],
     [0, 0, 1, 0, 1],
     [0, 1, 0, 0, 0],
     [0, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 1, 1, 0],
     [1, 1, 0, 1, 1],
     [1, 1, 1, 0, 0],]
CFeatures = ["A", "B", "C", "D"]

# Initialize an OrderedDict to map each feature to an ordered set of its values
featureValuesMap = OrderedDict()

# Initialize the mapping with each feature key pointing to an empty set
for feature in CFeatures:
    featureValuesMap[feature] = set()

# Populate the sets with values from C
for row in C:
    for i, feature in enumerate(CFeatures):
        featureValuesMap[feature].add(row[i])

# Convert sets to sorted lists
for feature in featureValuesMap:
    featureValuesMap[feature] = sorted(featureValuesMap[feature])

            