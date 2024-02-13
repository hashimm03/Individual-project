class TreeNode:
    def __init__(self, feature=None, value=None, left=None, right=None):
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.left = left        # Left child node
        self.right = right      # Right child node

class DecisionTree:
    def __init__(self, root=None):
        self.root = root        # Root node of the decision tree
    
    def addNode(node):
        pass

    def pathToLeaf(path):
        pass

def FindStrictExtStr(C, M, e):
    if (M == None):
        l0 = TreeNode(value=0)
        M0 = DecisionTree(root=l0)
        l1 = TreeNode(value=1)
        M1 = DecisionTree(root=l1)
    
        return M0, M1
    
    #X = empty tree
    # eLeaf = leaf of example following current tree?
    # path to eleaf represent as list?
    # e_ value of eLeaf

    # for all features e and e_ diagree on
        # M_ = extend tree for that specific example
        # l = new leaf for example e
        # A' = annotation of l
        # X = X + M_
        #
        # for all edges Pe
            #
    
    

