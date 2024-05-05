domain = "n"
if domain == "b":
    from dt import TreeNode, DecisionTree, FindStrictExtStr
    from config import C, CFeatures
else:
    from dt_integer import TreeNode, DecisionTree, FindStrictExtStr
    from config import C, CFeatures, orderFeatures

import math

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
    
    for tree in X:
        if(tree.countNodes() <= s):
            A = FindOptExtStr_BinarySearch(C, s, tree) # recursively call itself
            # if the tree returned by A is smaller than B or B is None
            if(A != None):
                return A
    return None

def FindMinimalTree_BinarySearch(C):
    """
    Uses binary search to find the smallest `s` such that a decision tree of size `s`
    can correctly classify all examples in C.
    
    Args:
        C ([[]]): Dataset of all examples, last index of each row is the classification
        M (DecisionTree): Initial decision tree (possibly None)
    
    Returns:
        DecisionTree: The smallest tree found within the optimal size or None if no such tree exists.
    """
    def ConstructTree(s, M):
        # Try to construct a tree with size `s`

        return FindOptModelStr_BinarySearch(C, s)
    
    # Find a reasonable upper bound for `s`, e.g., total number of nodes in a fully expanded tree
    if (domain == "b"):
        low, high = 1, int(math.pow(2,len(CFeatures) +1) - 1)   # example of a rough upper bound
    else:
        low, high = 1, int(math.pow(2,len(orderFeatures)+1) - 1)
    
    best_tree = None
    while low <= high:
        mid = (low + high) // 2
        tree = ConstructTree(mid, None)
        if tree is not None:
            best_tree = tree
            high = mid - 1  # Try for a smaller tree
        else:
            low = mid + 1  # Increase tree size
    
    return best_tree

def FindMinimalTree(C):
    """
    starting at size 1, looks for a decision tyree and increments s untill one is find or we are above the maximum
    
    Args:
        C ([[]]): Dataset of all examples, last index of each row is the classification
    
    Returns:
        DecisionTree: The smallest tree found within the optimal size or None if no such tree exists.
    """
    s = 0
    tree = None
    if(domain == "b"):
        max = int(math.pow(2,len(CFeatures) +1) - 1)
    else:
        max = int(math.pow(2,len(orderFeatures)+1) - 1)
    while tree is None and s<max:
        s += 1
        tree = FindOptModelStr(C, s)

    return tree

# usage
tree = FindMinimalTree_BinarySearch(C)
if(tree != None):
    tree.PrintTree() 
    tree.TestDecisionTree(C)

print("hsxbdw")
tree = FindMinimalTree(C)
if(tree != None):
    tree.PrintTree()
    tree.TestDecisionTree(C)
