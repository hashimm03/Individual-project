from dt import TreeNode, DecisionTree, FindStrictExtStr
from config import C, CFeatures
import math

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
            classification = M.Classification(e)

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

    # if size of M is above s return None
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

def FindOptModelStr_BinarySearch(C, s):
    # call other function passing None as M
    return FindOptExtStr_BinarySearch(C, s, None)


def FindOptExtStr_BinarySearch(C, s, M):
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
            classification = M.Classification(e)

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

    # if size of M is above s return None
    if(count >= s):
        return None
    # get array of extensions for M
    X = FindStrictExtStr(C, M, incorrectExample)
    
    B = None
    for tree in X:
        global countTree
        countTree += 1
        if(tree.countNodes() <= s):
            A = FindOptExtStr_BinarySearch(C, s, tree) # recursively call itself
            # if the tree returned by A is smaller than B or B is None
            if(A != None):
                B = A
                break
    
    return B

def FindOptimalTreeSize(C):
    """
    Uses binary search to find the smallest `s` such that a decision tree of size `s`
    can correctly classify all examples in C.
    
    Args:
        C ([[]]): Dataset of all examples, last index of each row is the classification
        M (DecisionTree): Initial decision tree (possibly None)
    
    Returns:
        DecisionTree: The smallest tree found within the optimal size or None if no such tree exists.
    """
    def canConstructTree(s, M):
        # Try to construct a tree with size `s`

        return FindOptModelStr_BinarySearch(C, s)
    
    # Find a reasonable upper bound for `s`, e.g., total number of nodes in a fully expanded tree
    low, high = 1, math.pow(2,len(C) +1) - 1   # example of a rough upper bound
    
    best_tree = None
    while low <= high:
        mid = (low + high) // 2
        tree = canConstructTree(mid, None)
        if tree is not None:
            best_tree = tree
            high = mid - 1  # Try for a smaller tree
        else:
            low = mid + 1  # Increase tree size
    
    return best_tree

def FindTreeSize(C):
    s = 0
    tree = None
    while tree is None:
        s += 1
        tree = FindOptModelStr(C, s)
    return tree

# usage
tree = FindOptimalTreeSize(C)
if(tree != None):
    print("final, binary", countTree)
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    
    tree.TestDecisionTree(C)

countTree = 0
tree = FindTreeSize(C)
if(tree != None):
    print("final", countTree)
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    
    tree.TestDecisionTree(C)
