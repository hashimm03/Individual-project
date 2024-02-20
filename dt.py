import config
class TreeNode:
    def __init__(self, feature=None, value=None, child0=None, child1=None):
        self.feature = feature  # Feature associated with the node
        self.value = value      # 0 or 1 if it's a leaf node, None otherwise
        self.child0 = child0      # Left child node
        self.child1 = child1      # Right child node
        if(self.value != None):
            self.annotation = getAnnotation(self)
    
    def getAnnotation(leaf):
        annotation = []

        return annotation

class DecisionTree:
    def __init__(self, root=None):
        self.root = root        # Root node of the decision tree
    
def FindStrictExtStr(C, M, e):
    if (M == None):
        l0 = TreeNode(value=0)
        M0 = DecisionTree(root=l0)
        l1 = TreeNode(value=1)
        M1 = DecisionTree(root=l1)
    
        return M0, M1
    
    X = None
    # eLeaf is a leaf that is given when running the example through the current tree
    # ePath is the path to get to this tree
    eLeaf = M.root
    ePath = []
    ePath.append(eLeaf)
    while(eLeaf.value == None ):
        for f in CFeatures:
            index = 0
            if f == eLeaf.feature:
                break

        if e[index] == 0:
            eLeaf = eLeaf.child0
        else:
            eLeaf = eLeaf.child1
        ePath.append(eLeaf)

    # e_ value of eLeaf
    e_ = eLeaf.examples[0]
    disagreeFeatures = []


    # for all features e and e_ diagree on - features that havent been considered in current tree?
        # M_ = extend tree for that feature
        # l = new leaf for feature
        # A' = annotation of l
        # X = X + M_ add this extension to X
        #
        # for all edges in epath
            #

    
    

