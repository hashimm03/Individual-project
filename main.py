from dt_integer import TreeNode, DecisionTree, FindStrictExtStr
from config import C, CFeatures

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
    countExamples = len(C)
    countCorrectExamples = 0

    # go through each example in dataset
    # Iterate over each example in C
    for e in C:  # Assuming C is your list of examples     
        if M != None:
            n = M.root  # Start from the root of the tree M

            # Navigate through the tree using example e
            while n.value is None:  # Continue until a leaf node is reached
                # Use .index() to find the index of the current feature directly
                index = CFeatures.index(n.feature)
                
                # Set n as its child based on the feature value
                if e[index] <= n.threshold:  # Assuming decisions are based on a threshold
                    n = n.childLeft
                else:
                    n = n.childRight

            # Check classification of e according to tree M
            if n.value == e[-1]:  # Assuming the last element in e is the true label
                countCorrectExamples += 1
            else:  # If e is incorrectly classified, return the incorrect example immediately
                incorrectExample = e
                break
        else:
            incorrectExample = e
            break

    # If all examples are correctly classified by M, return M
    if countCorrectExamples == len(C):
        return M
    
    # if M is a model for C
    # if all examples are correctly classified by M
    if(countCorrectExamples == countExamples):
        return M
    
    # calculate size of M, size is number of nodes in M
    if(M == None):
        count = 0
    else:
        count = M.countNodes()

    # if size of M s above s return None
    if(count >= s):
        return None
    # get array of extensions for M
    X = FindStrictExtStr(C, M, incorrectExample)
    
    B = None
    for tree in X:
        if(tree.countNodes() <= s):
            A = FindOptExtStr(C, s, tree) # recursively call itself
            # if the tree returned by A is smaller than B or B is None
            if(A != None and (B == None or B.countNodes() > A.countNodes())):
                B = A
    return B

# usage
tree = FindOptModelStr(C, 7)
if(tree != None):
    print("final")
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    
    tree.test_decision_tree( C, CFeatures)
