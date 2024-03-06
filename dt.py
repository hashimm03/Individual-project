from config import C, CFeatures
from copy import deepcopy

class TreeNode:
    def __init__(self, feature=None, value=None, child0=None, child1=None):
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.child0 = child0      # Left child node
        self.child1 = child1      # Right child node
    
    def DeepCopy(self):
        # Recursively copy the node and its children
        child0Copy = self.child0.DeepCopy() if self.child0 else None
        child1Copy = self.child1.DeepCopy() if self.child1 else None
        return TreeNode(self.feature, self.value, child0Copy, child1Copy)

class DecisionTree:
    def __init__(self, root=None):
        self.root = root        # Root node of the decision tree
        self.leafExampleMap = {}  # Stores examples for each leaf node

    def AddExampleToLeaf(self, leaf, example):
        if leaf.child0 is None and leaf.child1 is None:  # It's a leaf node
            leafID = id(leaf)  # Unique identifier for the node
            if leafID not in self.leafExampleMap:
                self.leafExampleMap[leafID] = []
            self.leafExampleMap[leafID].append(example)

    def getExampleForLeaf(self, leaf):
        node_id = id(leaf)
        examples = self.leafExampleMap.get(node_id, [])
        return examples[0] if examples else None
    
    def FindLeafAndPathForExample(self, example):
        eLeaf = self.root
        ePath = []
        ePath.append(eLeaf)
        while(eLeaf.value == None ):
            for f in CFeatures:
                index = 0
                if f == eLeaf.feature:
                    break

            if example[index] == 0:
                eLeaf = eLeaf.child0
            else:
                eLeaf = eLeaf.child1
            ePath.append(eLeaf)
        return eLeaf, ePath
    
    def DisagreeFeatures(self, example1, example2):
        disagree = []
        if example2 is None:
            print("Error:  examples 2 is None.")
            return []
        # Iterate over the feature values of both examples (excluding the classifier at the end)
        for i, (val1, val2) in enumerate(zip(example1[:-1], example2[:-1])):
            if val1 != val2:  # If the feature values disagree
                disagree.append(CFeatures[i])  # Append the feature name
        return disagree

    def removeExample(self, example):
        # Iterate over all leaf nodes stored in the leaf_example_map
        for node_id, examples in list(self.leafExampleMap.items()):
            if example in examples:
                examples.remove(example)  # Remove the example from the list

                # If the list becomes empty after removal, consider removing the key from the map
                if not examples:
                    del self.leafExampleMap[node_id]
                break  # Assuming each example only appears once, we can stop searching
    
    def DeepCopy(self):
        rootCopy = self.root.DeepCopy() if self.root else None
        treeCopy = DecisionTree(rootCopy)
        treeCopy.leafExampleMap = self.leafExampleMap.copy()  # Shallow copy might be sufficient here
        return treeCopy
    
    def computePath(self, target_node):
        """
        Compute the path from the root to the target_node.
        The path is a list of 0s and 1s, where 0 means 'go left' and 1 means 'go right'.
        """
        path = []
        stack = [(self.root, [])]  # Use self.root to access the root node of the tree instance

        while stack:
            current, current_path = stack.pop()

            if current is target_node:
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
        """
        current = copied_root
        for direction in path:
            if direction == 0:
                current = current.child0
            else:  # direction == 1
                current = current.child1
            if current is None:
                return None  # Path leads to a non-existent node, likely an error in path computation
        return current
    
    def countNodes(self):
        def count(n):
            if n is None:
                return 0
            return 1 + count(n.child0) + count(n.child1)
        
        return count(self.root)
    
    def PrintTree(self, node=None, prefix=""):
        if node is None:
            node = self.root

        if node.value is not None:  # It's a leaf node
            print(f"{prefix}Leaf: {node.value}")
        else:
            # Print the current node's feature
            print(f"{prefix}Node: {node.feature}")
            # Recursively print the left child
            self.PrintTree(node.child0, prefix + "  0-> ")
            # Recursively print the right child
            self.PrintTree(node.child1, prefix + "  1-> ")

    
def FindStrictExtStr(C, M, e):
    if (M == None):
        l0 = TreeNode(value=0)
        M0 = DecisionTree(root=l0)
        l1 = TreeNode(value=1)
        M1 = DecisionTree(root=l1)
        for example in C:
            M0.AddExampleToLeaf(l0, example)
            M1.AddExampleToLeaf(l1, example)
    
        return [M0, M1]
    X = []
    # This function needs to be adjusted to track the features used along the path
    eLeaf, ePath = M.FindLeafAndPathForExample(e)
    usedFeatures = set(node.feature for node in ePath if node.feature is not None)
    
    e_ = M.getExampleForLeaf(eLeaf)

    disagreeFeatures = [f for f in M.DisagreeFeatures(e, e_) if f not in usedFeatures]
    
    for feature in disagreeFeatures:
        # Assuming featureIndex is correctly determined here...
        featureIndex = CFeatures.index(feature)
        
        # Create new node and leaf based on disagreement
        l = TreeNode(value=e[-1])
        if e[featureIndex] == 0:
            n = TreeNode(feature=feature, child0=l, child1=M.root)
        else:
            n = TreeNode(feature=feature, child0=M.root, child1=l)

        M_ = DecisionTree(root = n)

        # adding the annotation
        M_.leafExampleMap = deepcopy(M.leafExampleMap)
        # remove example from leaf it was at previously
        M_.removeExample(e)
        # add example to new node
        M_.AddExampleToLeaf(l, e)

        X.append(M_)

        # for each node in path
        for i in range(len(ePath)-1):
            print("qqqqq")
            featureIndex = 0
            for f in CFeatures:
                if f == ePath[i].feature:
                    break
                featureIndex += 1
            
             # first make copy of M

            if ePath[i].value == None: # not a leaf
                M_copy = M.DeepCopy()
                pathToTarget = M.computePath(ePath[i])
                copyEPathNode = M.findEquivalentNode(M_copy.root, pathToTarget)
                pathToTargetChild = M.computePath(ePath[i+1])
                copyEPathNodeChild = M.findEquivalentNode(M_copy.root, pathToTargetChild)
                
                l = TreeNode(value = e[-1]) # leaf with value equal to example classification
                if e[featureIndex] == 0: # if it is a 0 edge make new node with 0child leaf and 1 child next node in path
                    n = TreeNode(feature=feature, child0 = l, child1 = copyEPathNodeChild )
                else:
                    n = TreeNode(feature=feature, child0 = copyEPathNodeChild, child1 = l)
                
                # now we need to set the node in paths child to n
                
                if e[featureIndex] == 0:
                    copyEPathNode.child0 = n
                else:
                    copyEPathNode.child1 = n
                
                # adding the annotation
                M_copy.leafExampleMap = deepcopy(M.leafExampleMap)
                # remove example from leaf it was at previously
                M_copy.removeExample(e)
                # add example to new node
                M_copy.AddExampleToLeaf(l, e)
                X.append(M_copy)
    
    return X
                
            

    
    

