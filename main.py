from dt import TreeNode, DecisionTree, FindStrictExtStr
from config import C, CFeatures

countTree = 0
def FindOptModelStr(C, s):
    # call other function passing None as M
    return FindOptExtStr(C, s, None)

def FindOptExtStr(C, s, M):
    """
    Finds smallest possible decision tree that correctly classifies all examples in C

    Args:
        C([[]]): dataset of all examples, last index of each row is the classification
        s(int): maximum size of tree, number of nodes
        M(DecisionTree): decision tree
    """
    # initialise variables
    incorrectExample = None
    countCorrectExamples = 0

    # go through each example in dataset
    # Iterate over each example in C
    for e in C:  # Assuming C is your list of examples     
        if M != None:

            #check the classification of e according to the model M 
            classification = M.predict(e)

            # Check classification of e according to tree M
            if classification == e[-1]:  # Assuming the last element in e is the true label
                countCorrectExamples += 1
            else:  # If e is incorrectly classified, return the incorrect example immediately
                incorrectExample = e
                break
        else:
            incorrectExample = e
            break

    
    # calculate size of M, size is number of nodes in M
    if(M == None):
        count = 0
    else:
        count = M.countNodes()

    if(countCorrectExamples == len(C)):
        return M

    # if size of M s above s return None
    if(count >= s):
        return None
    # get array of extensions for M
    X = FindStrictExtStr(C, M, incorrectExample)
    
    B = None
    for tree in X:
        global countTree
        countTree += 1
        if(tree.countNodes() <= s):
            A = FindOptExtStr(C, s, tree) # recursively call itself
            # if the tree returned by A is smaller than B or B is None
            if(A != None and (B == None or B.countNodes() > A.countNodes())):
                B = A
    
    return B

# usage
tree = FindOptModelStr(C, 9)
if(tree != None):
    print("final", countTree)
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    
    tree.TestDecisionTree(C)
