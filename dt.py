import config
class TreeNode:
    def __init__(self, feature=None, value=None, child0=None, child1=None):
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.child0 = child0      # Left child node
        self.child1 = child1      # Right child node

class DecisionTree:
    def __init__(self, root=None):
        self.root = root        # Root node of the decision tree
        self.leafExampleMap = {}  # Stores examples for each leaf node

    def AddExampleToLeaf(self, leaf, example):
        if leaf.left is None and leaf.right is None:  # It's a leaf node
            leafID = id(leaf)  # Unique identifier for the node
            if leafID not in self.leafExampleMap:
                self.leafExampleMap[leafID] = []
            self.leafExampleMap[leafID].append(example)

    def getExampleForLeaf(self, leaf):
        node_id = id(leaf)
        examples = self.leafExampleMap.get(node_id, [])
        return examples[0] if examples else None
    
    def findLeafAndPathForExample(self, example):
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
        # Iterate over the feature values of both examples (excluding the classifier at the end)
        for i, (val1, val2) in enumerate(zip(example1[:-1], example2[:-1])):
            if val1 != val2:  # If the feature values disagree
                disagree.append(self.features[i])  # Append the feature name
        return disagree
        
    
def FindStrictExtStr(C, M, e):
    if (M == None):
        l0 = TreeNode(value=0)
        M0 = DecisionTree(root=l0)
        l1 = TreeNode(value=1)
        M1 = DecisionTree(root=l1)
        for example in C:
            M0.AddExampleToLeaf(l0, example)
            M1.AddExampleToLeaf(l1, example)
    
        return M0, M1
    
    X = None
    # eLeaf is a leaf that is given when running the example through the current tree
    # ePath is the path to get to this tree
    eLeafAndPath = M.FindLeafAndPathForExample(example)
    eLeaf = eLeafAndPath[0]
    ePath = eLeafAndPath[1]

    # e_ example that reaches eLeaf
    e_ = M.getExampleForLeaf(eLeaf)
    disagreeFeatures = M.DisagreeFeatures(e, e_)


    # for all features e and e_ diagree on
    for features in disagreeFeatures:
        for f in CFeatures:
            index = 0
            if f == eLeaf.feature:
                break

        l = TreeNode(value = [e[-1]])
        if e[i] == 0:
            n = TreeNode(feature=features, child0 = l, child1 =M.root )
        else:
            n = TreeNode(feature=features, child0 = M.root, child1 = l)
        
        M_ = DecisionTree(root = n)
        M_.leafExampleMap = M.leafExampleMap
        M_.AddExampleToLeaf(l, e)
        

        X.append(M_)

    
    

