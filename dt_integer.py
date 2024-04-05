from config import C, CFeatures, featureValuesMap
from copy import deepcopy

class TreeNode:
    nextID = 0
    def __init__(self, feature=None, value=None, childLeft=None, childRight=None, threshold=None):
        """
        Initialiser for the class which defines a node in the tree
        
        Args:
            feature (string): For nodes which are not leafs, the feature of that node, None for leafs
            value (int): for leafs of the tree, None for other nodes, value of 1 or 0
            childLeft (TreeNode): 0 branch child of node
            childRight (TreeNode): 1 branch child of node
        
        """
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.childLeft = childLeft      # Left child node
        self.childRight = childRight      # Right child node
        self.id = TreeNode.nextID
        self.threshold = threshold # thresehold which we compare the example values to
        TreeNode.nextID += 1 # setting id so when making copies the nodes have same examples assigned
    
    def DeepCopy(self):
        """
        Recursively copies the node and its children

        """
        childLeftCopy = self.childLeft.DeepCopy() if self.childLeft else None
        childRightCopy = self.childRight.DeepCopy() if self.childRight else None
        nodeCopy =  TreeNode(self.feature, self.value, childLeftCopy, childRightCopy)
        nodeCopy.id = self.id
        return nodeCopy

class DecisionTree:
    def __init__(self, root=None):
        """
        Initialiser for the class which defines the full tree
        
        Args:
            root (TreeNode): the node which is the root of the decision tree
        
        """
        self.root = root        
        self.leafExampleMap = {}  # Stores examples for each leaf node
        self.features = set() # features that have already been split, helps to avoid splittin by same feature in same branch

    def AddExampleToLeaf(self, leaf, example):
        """
        Edits the hashmap leafExampleMap, and adds the leaf if it doesnt already exist and assignss an example to it
        
        Args:
            leaf (TreeNode): the leaf we going to add to the hashmap
            example (int[]): example that reaches this leaf
        
        """
        if leaf.childLeft is None and leaf.childRight is None:  # It's a leaf node
            self.leafExampleMap[leaf.id] = [example] # assign example to leaf

    def getExampleForLeaf(self, leaf):
        """
        Returns an example that gets to a leaf, from the hashmap

        Args:
            leaf (TreeNode): leaf that we want example from

        Returns:
            one example if there is one
        """
        examples = self.leafExampleMap.get(leaf.id, [])
        return examples if examples else None # return first example as we only need 1 or None if there are no examples at that leaf
    
    def FindLeafAndPathForExample(self, example):
        """
        Traverses through the decision tree with an example, and stores the path in a list and the leaf it reaches.
        
        Args:
            example ([]): example from the dataset.
        
        Returns:
            the leaf that the example reaches,
            an array which stores the path the example took on the tree.
        """
        eLeaf = self.root
        ePath = []
        ePath.append(eLeaf) # Adds the root to the path.
        while eLeaf.value is None: # While it's not a leaf.
            featureIndex = CFeatures.index(eLeaf.feature) # Find index of the feature that we are currently looking at.
            
            # Based on value stored in example for that feature, traverse through the tree.
            if example[featureIndex] <= eLeaf.threshold:
                eLeaf = eLeaf.childLeft
            else:
                eLeaf = eLeaf.childRight
                
            # Add each node to the path.
            ePath.append(eLeaf)
            
        return eLeaf, ePath
    
    def DisagreeFeatures(self, example1, example2):
        """
        Identify features where two examples have values on either side of the thresholds
        defined in featureValuesMap.
        For each differing feature, return a 2D list where each 
        inner list contains the feature name and a single threshold value from the values 
        that are between the two example values.
        
        Args:
            example1 (list): An example from the dataset; e.g., a row in C.
            example2 (list): Another example from the dataset; different from example1.


        Returns:
            list: A 2D list where each inner list contains the feature name and a single
                threshold value, for each value between the example values.
        """
        disagree = []
        for i, feature in enumerate(CFeatures):
            val1, val2 = example1[i], example2[i]
            if val1 != val2:  # Check if values differ
                # Find and iterate through values between val1 and val2
                for val in featureValuesMap[feature]:
                    if min(val1, val2) <= val < max(val1, val2):
                        disagree.append((feature, val))
                    
        return disagree

    def removeExample(self, example):
        """
        removes example from leaf, used when extending tree we assign example to a new leaf so should remove it from where it previously was

        Args:
            example ([]): example from the dataset

        """
        # Iterate over all leaf nodes stored in the leaf_example_map
        for leafID,  examples in self.leafExampleMap.items():
            if example in examples:
                examples.remove(example)  # Remove the example from the list
    
    def DeepCopy(self):
        """
        creates deep copy of decision tree, so we can make extensions and modifications without making changes to original tree

        """
        rootCopy = self.root.DeepCopy() if self.root else None # create copy of root and all child nodes using DeepCopy() function
        treeCopy = DecisionTree(rootCopy) # make new decision tree with copied root
        treeCopy.leafExampleMap = self.leafExampleMap.copy()
        treeCopy.features = self.features.copy()
        return treeCopy
    
    def computePath(self, targetNode):
        """
        Compute the path from the root to the target_node.
        The path is a list of 0s and 1s, where 0 means 'go left' and 1 means 'go right'.

        Args:
            targetNode(TreeNode): the node we are computing a path to
        
        Returns:
            array of 0s and 1s which is the path to the target node
        """
        path = []
        stack = [(self.root, [])]  # Use self.root to access the root node of the tree

        # performs depth first search
        while stack:
            current, current_path = stack.pop()

            if current is targetNode:
                return current_path

            if current.childRight is not None:
                stack.append((current.childRight, current_path + [1]))

            if current.childLeft is not None:
                stack.append((current.childLeft, current_path + [0]))

        return path
    
    def findEquivalentNode(self, copied_root, path):
        """
        Given the root of a copied tree and a path (list of 0s and 1s),
        navigate through the tree following the path to find the equivalent node.

        Args:
            copied_root (TreeNode): the root of the copied tree
            path(array): path consisting of 0s and 1s to get to the node
        """
        current = copied_root
        for direction in path: # follow the path
            if direction == 0:
                current = current.childLeft
            else:  # direction == 1
                current = current.childRight
            if current is None:
                return None  # Path leads to a non-existent node, likely an error in path computation
        return current
    
    def countNodes(self):
        """
        counts the number of nodes in the decision tree using recursion

        return:
             the number of nodes in the tree
        """
        def count(n):
            if n is None:
                return 0
            """elif n.value is not None:
                return 1"""
            return 1 + count(n.childLeft) + count(n.childRight) # recursively call itself to count its children nodes
        
        return count(self.root)
    
    def PrintTree(self, node=None, prefix="", isLast=True, branchType=None):
        if node is None:
            node = self.root

        # Connector and branch indicator based on the branch type.
        connector = "└── " if isLast else "├── "
        branchIndicator = ""
        if branchType == 0:
            branchIndicator = "[<=] "
        elif branchType == 1:
            branchIndicator = "[>] "

        # Prepare the prefix for the next level of recursion.
        next_prefix = prefix + ("    " if isLast else "│   ")

        # Handling for leaf nodes.
        if node.value is not None:  # It's a leaf node.
            examples = self.getExampleForLeaf(node)
            examples_str = ", ".join([str(e) for e in examples]) if examples else "No examples"
            print(f"{prefix}{connector}{branchIndicator}Leaf: {node.value} -> Examples: {examples_str}")
        else:
            # For non-leaf nodes, display the node's decision criterion.
            node_description = f"Node: {node.feature} ? {node.threshold}"
            print(f"{prefix}{connector}{branchIndicator}{node_description}")

            # Recursively print the left child (if it exists), signifying the branch for values <= threshold.
            if node.childLeft is not None:
                self.PrintTree(node.childLeft, next_prefix, False, 0)

            # Recursively print the right child (if it exists), signifying the branch for values > threshold.
            if node.childRight is not None:
                self.PrintTree(node.childRight, next_prefix, True, 1)
        
    def predict(self, example, CFeatures):
        """
        Traverses the decision tree to predict the outcome for a given example.
        
        :param tree: The root node of the decision tree (instance of TreeNode).
        :param example: A list of feature values for which to predict the outcome.
        :param feature_names: A list of feature names corresponding to the indexes in 'example'.
        
        :return: The prediction at the leaf node reached by traversing the tree.
        """
        current_node = self.root
        while current_node.value is None:  # Continue until a leaf node is reached
            # Get the index of the current feature in the example
            feature_index = CFeatures.index(current_node.feature)
            # Move to the next node based on the feature value in the example
            if example[feature_index] <= current_node.threshold:
                current_node = current_node.childLeft
            else:
                current_node = current_node.childRight
        return current_node.value  # Return the prediction
    
    def test_decision_tree(self, dataset, CFeatures):
        """
        Tests the decision tree on a dataset and prints the outcome for each example.

        :param tree: The root node of the decision tree.
        :param dataset: The dataset to test, where each example includes feature values and the actual outcome as the last element.
        :param feature_names: A list of feature names corresponding to the indexes in the examples.
        """
        correct_predictions = 0
        for example in dataset:
            # Separate features and actual outcome
            features, actual = example[:-1], example[-1]
            # Get the prediction for the current example
            predicted = self.predict(features, CFeatures)
            # Check if the prediction is correct
            if predicted == actual:
                correct_predictions += 1
                print(f"Example: {features} | Predicted: {predicted} = Actual: {actual} (Correct)")
            else:
                print(f"Example: {features} | Predicted: {predicted} != Actual: {actual} (Incorrect)")
        
        # Print the overall accuracy
        accuracy = correct_predictions / len(dataset)
        print(f"\nAccuracy: {accuracy:.2f} ({correct_predictions}/{len(dataset)})")
    
    def validatePath(self, node, decisions={}):
        # Base case: If node is None, return True (empty path is trivially valid)
        if node is None:
            return True

        # If it's a leaf node, validate the examples assigned to this leaf
        if node.childLeft is None and node.childRight is None:
            examples = self.getExampleForLeaf(node)
            if examples is None:
                # No examples to validate, consider it valid
                return True
            for example in examples:
                # Check each example against the decisions made on the path to this leaf
                for feature, (threshold, direction) in decisions.items():
                    feature_index = CFeatures.index(feature)
                    if direction == "left" and not example[feature_index] <= threshold:
                        return False  # Example doesn't match the decision to go left
                    if direction == "right" and not example[feature_index] > threshold:
                        return False  # Example doesn't match the decision to go right
            return True  # All examples for this leaf are consistent with the path's decisions

        # Recursive case: Check both children, updating decisions with the current node's feature
        if node.feature is not None:
            # Copy decisions to avoid mutating the original as we go down different paths
            decisions_left = decisions.copy()
            decisions_right = decisions.copy()

            # Update decisions with the current node's threshold for the left and right paths
            decisions_left[node.feature] = (node.threshold, "left")  # Decision to go left if <= threshold
            decisions_right[node.feature] = (node.threshold, "right")  # Decision to go right if > threshold
            
            # Validate paths to the left and right children
            valid_left = self.validatePath(node.childLeft, decisions_left)
            valid_right = self.validatePath(node.childRight, decisions_right)

            # Return True if both paths are valid, False otherwise
            return valid_left and valid_right

        # If the current node is not a leaf and has no feature, something is wrong
        return False

    
def FindStrictExtStr(C, M, e):
    """
    finds a full set of extensions for M and example e

    Args:
        M(DecisionTree): decision tree we are going to extend
        e([]): example from dataset
    
    Return:
        Array of different decision trees which are extensions of M
    """
    # creates 2 decision trees consisting of 1 node, one with value 0 and one with value of 1
    if (M == None):
        l0 = TreeNode(value=0)
        M0 = DecisionTree(root=l0)
        l1 = TreeNode(value=1)
        M1 = DecisionTree(root=l1)
        for example in C:
            if example[-1] == 1:
                M1.AddExampleToLeaf(l1, example)
            else:
                M0.AddExampleToLeaf(l0, example)

        return [M0, M1]
    X = []

    # navigate through decision tree using example and store the end leaf and path
    eLeaf, ePath = M.FindLeafAndPathForExample(e)
    # features that have already been considered in pathj
    usedFeatures = set(node.feature for node in ePath if node.feature is not None)

    # get example assigned to eleaf
    e_ = M.getExampleForLeaf(eLeaf)[0] if M.getExampleForLeaf(eLeaf) is not None else None

    # features that have a different value for e and e_
    disagreeFeatures = [f for f in M.DisagreeFeatures(e, e_) if f not in usedFeatures]
    print("all - ",disagreeFeatures, e, e_)
    
    for feature in disagreeFeatures:
        if feature[0] not in M.features: # find index of feature
            print("current tree:")
            M.PrintTree()
            print("current- ",feature)
            featureIndex = CFeatures.index(feature[0])
            
            # Create new node and leaf based on disagreement
            l = TreeNode(value=e[-1])
            if e[featureIndex] <= feature[1]:
                n = TreeNode(feature=feature[0], childLeft=l, childRight=M.root, threshold=feature[1])
            else:
                n = TreeNode(feature=feature[0], childLeft=M.root, childRight=l, threshold = feature[1])

            # create new decision tree with new root
            M_ = DecisionTree(root = n)
            M_.leafExampleMap = M.leafExampleMap.copy()
            M_.features = M.features.copy()
            M_.features.add(feature)

            # add example to new node
            M_.AddExampleToLeaf(l, e)
            print("ext 1")
            M_.PrintTree()

            if M_.validatePath(n ,{}):
            # first type of extension
                X.append(M_)
            else:
                continue

        # for each node in path
        for i in range(len(ePath)-1):
            featureIndex = CFeatures.index(ePath[i].feature)
            
            # first make copy of M
            M_copy = deepcopy(M)
            M_copy.features = M.features.copy()
            pathToTarget = M.computePath(ePath[i])
            copyEPathNode = M.findEquivalentNode(M_copy.root, pathToTarget)
            pathToTargetChild = M.computePath(ePath[i+1])
            copyEPathNodeChild = M.findEquivalentNode(M_copy.root, pathToTargetChild)

            if ePath[i].value == None: # not a leaf
                l = TreeNode(value = e[-1]) # leaf with value equal to example classification
                if e[featureIndex] <= feature[1]: # if it is a 0 edge make new node with 0child leaf and 1 child next node in path
                    n = TreeNode(feature=feature[0], childLeft = l, childRight = copyEPathNodeChild, threshold=feature[1])
                else:
                    n = TreeNode(feature=feature[0], childLeft = copyEPathNodeChild, childRight = l, threshold=feature[1])

                # now we need to set the node in paths child to n
                if e[featureIndex] <= ePath[i].threshold:
                    copyEPathNode.childLeft = n
                else:
                    copyEPathNode.childRight = n
                
                M_copy.features.add(feature)
                # add example to new node
                M_copy.AddExampleToLeaf(l, e)

                print("ext 2")
                M_copy.PrintTree()
                # second type of extension
                if M_copy.validatePath(n ,{}):
                    X.append(M_copy)
                else:
                    continue
    
    return X