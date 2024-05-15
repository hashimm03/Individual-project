from config import C, CFeatures
from copy import deepcopy

class TreeNode:
    nextID = 0
    def __init__(self, feature=None, value=None, child0=None, child1=None):
        """
        Initialiser for the class which defines a node in the tree
        
        Args:
            feature (string): For nodes which are not leafs, the feature of that node, None for leafs
            value (int): for leafs of the tree, None for other nodes, value of 1 or 0
            child0 (TreeNode): 0 branch child of node
            child1 (TreeNode): 1 branch child of node
        
        """
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.child0 = child0      # Left child node
        self.child1 = child1      # Right child node
        self.id = TreeNode.nextID
        TreeNode.nextID += 1 # setting id so when making copies the nodes have same examples assigned

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
        if leaf.child0 is None and leaf.child1 is None:  # It's a leaf node
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
        traverses through the decision tree with and example, and stores the path in a list and the leaf it reaches

        Args:
            example ([]): example from the dataset

        Returns:
            the leaf that the example reaches,
            an array which stores the path the example took on the tree
        """
        eLeaf = self.root
        ePath = []
        ePath.append(eLeaf) # adds the root to the path
        while(eLeaf.value == None ): # while its not a leaf
            index = CFeatures.index(eLeaf.feature)

            # based on value stored in example for that feature traverse through the tree
            if example[index] == 0:
                eLeaf = eLeaf.child0
            else:
                eLeaf = eLeaf.child1
            # add each node to the path
            ePath.append(eLeaf)
        return eLeaf, ePath
    
    def DisagreeFeatures(self, example1, example2):
        """
        return all the features that 2 examples dont have the same value for

        Args:
            example1 ([]): example from the dataset, would be e in the main loop
            example2 ([]): example from the dataset, would be e_ in the main loop

        Returns:
            an array which has all the features that the two examples disagree on
        """
        disagree = []
        if example2 is None: # if e_ has no examples return an empty list
            print("Error:  examples 2 is None.")
            return []
        if example1 is None: # if e_ has no examples return an empty list
            print("Error:  examples 1 is None.")
            return []
        # Iterate over the feature values of both examples (excluding the classifier at the end)
        for i, (val1, val2) in enumerate(zip(example1[:-1], example2[:-1])):
            if val1 != val2:  # If the feature values disagree
                disagree.append(CFeatures[i])  # Append the feature name
        return disagree
    
    def ComputePath(self, targetNode):
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

            if current.child1 is not None:
                stack.append((current.child1, current_path + [1]))

            if current.child0 is not None:
                stack.append((current.child0, current_path + [0]))

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
                current = current.child0
            else:  # direction == 1
                current = current.child1
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
            return 1 + count(n.child0) + count(n.child1) # recursively call itself to count its children nodes
        
        return count(self.root)
    
    def PrintTree(self, node=None, prefix="", isLast=True, branchType = None):
        """
        prints the tree to the terminal

        """
        if node is None:
            node = self.root
        
        # Determine the appropriate connector based on isLast
        connector = "└── " if isLast else "├── "
        branchIndicator = "[1] " if branchType == 1 else "[0] " if branchType == 0 else ""

        # Prepare the next prefix for child nodes
        next_prefix = prefix + ("    " if isLast else "│   ")

        if node.value is not None:  # If it's a leaf node
            print(f"{prefix}{connector}{branchIndicator}Leaf: {node.value}", self.getExampleForLeaf(node))
        else:
            print(f"{prefix}{connector}{branchIndicator}Node: {node.feature}")
            # Recursively print the left child (if exists), indicating it as a 0 branch
            if node.child0 is not None:
                self.PrintTree(node.child0, next_prefix, node.child1 is None, branchType=0)
            # Recursively print the right child (if exists), indicating it as a 1 branch
            if node.child1 is not None:
                self.PrintTree(node.child1, next_prefix, True, branchType=1)

    def Classification(self, example):
        """
        Traverses the decision tree to predict the outcome for a given example.
        
        Args:
            tree(DecisionTree): The root node of the decision tree (instance of TreeNode).
            example([]): A list of feature values for which to predict the outcome.
        
        returns:
            The prediction at the leaf node reached by traversing the tree.
        """
        current_node = self.root
        while current_node.value is None:  # Continue until a leaf node is reached
            # Get the index of the current feature in the example
            feature_index = CFeatures.index(current_node.feature)
            # Move to the next node based on the feature value in the example
            if example[feature_index] == 0:
                current_node = current_node.child0
            else:
                current_node = current_node.child1
        return current_node.value  # Return the prediction
    
    def TestDecisionTree(self, dataset):
        """
        Tests the decision tree on a dataset and prints the outcome for each example.

        Args:
            tree(DecisionTree): The root node of the decision tree.
            dataset[[]]: The dataset to test, where each example includes feature values and the actual outcome as the last element.
        """
        correct_predictions = 0
        for example in dataset:
            # Separate features and actual outcome
            features, actual = example[:-1], example[-1]
            # Get the prediction for the current example
            predicted = self.Classification(features)
            # Check if the prediction is correct
            if predicted == actual:
                correct_predictions += 1
                print(f"Example: {features} | Predicted: {predicted} = Actual: {actual} (Correct)")
            else:
                print(f"Example: {features} | Predicted: {predicted} != Actual: {actual} (Incorrect)")
        
        # Print the overall accuracy
        accuracy = correct_predictions / len(dataset)
        print(f"\nAccuracy: {accuracy:.2f} ({correct_predictions}/{len(dataset)})")

    
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
    # to avoid extending by features already considered
    usedFeatures = set(node.feature for node in ePath if node.feature is not None)
    
    # get example assigned to eleaf
    e_ = M.getExampleForLeaf(eLeaf)[0] if M.getExampleForLeaf(eLeaf) is not None else None
    # features that have a different value for e and e_
    disagreeFeatures = [f for f in M.DisagreeFeatures(e, e_)if f not in usedFeatures] # if f not in usedFeatures optimisation
    
    for feature in disagreeFeatures:
        #if feature not in M.features: # optimisation
        featureIndex = CFeatures.index(feature)

        # only extend by features if index of node n is smaller than child node index
        #if(M.root.feature is None or featureIndex < CFeatures.index(M.root.feature)): # optimisation for symmetry
                        
            # Create new node and leaf based on disagreement
        l = TreeNode(value=e[-1])
        if e[featureIndex] == 0:
            n = TreeNode(feature=feature, child0=l, child1=M.root)
        else:
            n = TreeNode(feature=feature, child0=M.root, child1=l)

        # create new decision tree with new root
        M_ = DecisionTree(root = n)
        M_.leafExampleMap = M.leafExampleMap.copy()
        M_.features = M.features.copy()
        M_.features.add(feature)

        # add example to new node
        M_.AddExampleToLeaf(l, e)

        X.append(M_)

        # for each node in path
        for i in range(len(ePath)-1):         
            # first make copy of M
            M_copy = deepcopy(M)
            M_copy.features = M.features.copy()
            pathToTarget = M.ComputePath(ePath[i])
            copyEPathNode = M.findEquivalentNode(M_copy.root, pathToTarget)
            pathToTargetChild = M.ComputePath(ePath[i+1])
            copyEPathNodeChild = M.findEquivalentNode(M_copy.root, pathToTargetChild)

            # only extend by features if index of node n is smaller than child node index
            #if(copyEPathNodeChild.feature is None or (CFeatures.index(feature)< CFeatures.index(copyEPathNodeChild.feature) and CFeatures.index(feature) > CFeatures.index(copyEPathNode.feature))): # optimisation for symmetry
            if ePath[i].value == None: # not a leaf
                l = TreeNode(value = e[-1]) # leaf with value equal to example classification
                if e[CFeatures.index(feature)] == 0: # if it is a 0 edge make new node with 0child leaf and 1 child next node in path
                    n = TreeNode(feature=feature, child0 = l, child1 = copyEPathNodeChild )
                else:
                    n = TreeNode(feature=feature, child0 = copyEPathNodeChild, child1 = l)
                    
                # now we need to set the node in paths child to n
                if e[CFeatures.index(ePath[i].feature)] == 0:
                    copyEPathNode.child0 = n
                else:
                    copyEPathNode.child1 = n
                    
                M_copy.features.add(feature)
                # add example to new node
                M_copy.AddExampleToLeaf(l, e)
                X.append(M_copy)
                    
    
    return X