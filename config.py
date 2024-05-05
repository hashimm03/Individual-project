from collections import OrderedDict

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

C = [[5.1,3.5,1.4,0.2,"Iris-setosa"],
[4.9,3.0,1.4,0.2,"Iris-setosa"],
[4.7,3.2,1.3,0.2,"Iris-setosa"],
[7.0,3.2,4.7,1.4,"Iris-versicolor"],
[6.4,3.2,4.5,1.5,"Iris-versicolor"],
[6.9,3.1,4.9,1.5,"Iris-versicolor"],
[6.3,3.3,6.0,2.5,"Iris-virginica"],
[5.8,2.7,5.1,1.9,"Iris-virginica"],
[7.1,3.0,5.9,2.1,"Iris-virginica"]]
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

orderFeatures = []
for key, values in featureValuesMap.items():
    for value in values:
        orderFeatures.append([key, value])
