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

C = [[0,1,0,0,0,1,0,1,1],
     [0,1,0,1,0,0,0,1,1],
     [1,0,0,0,1,0,1,1,0],
     [0,0,1,0,0,1,0,0,1],
     [1,0,0,1,0,0,0,0,1],
     [0,1,0,1,0,0,1,0,0],
     [0,1,0,1,0,0,1,1,1],
     [0,0,1,0,1,0,1,1,1],
     [1,0,0,1,0,0,1,1,0],
     [1,0,0,0,0,1,0,1,1],
     [0,0,1,1,0,0,1,0,1],
     [1,0,0,0,1,0,1,0,0]]
CFeatures = ["sunny", "rain", "overcast", "temp:Mild", "temp:Hot", "temp:Cool", "humid", "windy"]
"""

C = [[1, 1, 1],
     [1, 0, 0],
     [0, 1, 0],
     [0, 0, 0],]
CFeatures = ["Fur", "Barks"]



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
    [5, 8, 7, 10, 1],
    [3, 6, 2, 9, 0],
    [6, 9, 5, 12, 1],
    [2, 4, 8, 8, "red"],
    [7, 7, 6, 11, 1],    
    [4, 5, 3, 7, 0],
    [8, 10, 4, 13, 1],
    [1, 3, 9, 6, 2],
    [2, 4, 8, 7, 1]
]
CFeatures = ["A", "B", "C", "D"]


C = [[5.1,3.5,1.4,0.2,"Iris-setosa"],
[4.8,3.1,1.6,0.2,"Iris-setosa"],
[5.4,3.4,1.5,0.4,"Iris-setosa"],
[5.2,4.1,1.5,0.1,"Iris-setosa"],
[5.5,4.2,1.4,0.2,"Iris-setosa"],
[4.9,3.1,1.5,0.1,"Iris-setosa"],
[5.0,3.2,1.2,0.2,"Iris-setosa"],
[5.5,3.5,1.3,0.2,"Iris-setosa"],
[4.9,3.1,1.5,0.1,"Iris-setosa"],
[4.4,3.0,1.3,0.2,"Iris-setosa"],
[5.1,3.4,1.5,0.2,"Iris-setosa"],
[5.0,3.5,1.3,0.3,"Iris-setosa"],
[6.3,2.3,4.4,1.3,"Iris-versicolor"],
[5.6,3.0,4.1,1.3,"Iris-versicolor"],
[5.5,2.5,4.0,1.3,"Iris-versicolor"],
[5.5,2.6,4.4,1.2,"Iris-versicolor"],
[6.1,3.0,4.6,1.4,"Iris-versicolor"],
[5.8,2.6,4.0,1.2,"Iris-versicolor"],
[5.0,2.3,3.3,1.0,"Iris-versicolor"],
[5.6,2.7,4.2,1.3,"Iris-versicolor"],
[5.7,3.0,4.2,1.2,"Iris-versicolor"],
[5.7,2.9,4.2,1.3,"Iris-versicolor"],
[6.2,2.9,4.3,1.3,"Iris-versicolor"],
[5.1,2.5,3.0,1.1,"Iris-versicolor"],
[5.7,2.8,4.1,1.3,"Iris-versicolor"],
[6.3,3.3,6.0,2.5,"Iris-virginica"],
[5.8,2.7,5.1,1.9,"Iris-virginica"],
[6.0,2.2,5.0,1.5,"Iris-virginica"],
[6.9,3.2,5.7,2.3,"Iris-virginica"],
[5.6,2.8,4.9,2.0,"Iris-virginica"],
[7.7,2.8,6.7,2.0,"Iris-virginica"],
[6.3,2.7,4.9,1.8,"Iris-virginica"],
[6.7,3.3,5.7,2.1,"Iris-virginica"],
[7.2,3.2,6.0,1.8,"Iris-virginica"],
[6.2,2.8,4.8,1.8,"Iris-virginica"]]
CFeatures = ["A", "B", "C", "D"]
"""
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