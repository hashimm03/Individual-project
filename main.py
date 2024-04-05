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
    for e in C:
        if(M != None):
            n = M.root
            #navigate through tree using example e
            while(n.value == None ):
                # find index of feature
                index = 0
                for f in CFeatures:
                    if f == n.feature:
                        break
                    index += 1
                # sets n as its child
                if e[index] == 0:
                    n = n.childLeft
                else:
                    n = n.childRight

            # checks classification of e according to tree M
            if n.value == e[-1]:
                countCorrectExamples += 1
            else: # if e is incorrectly classified break
                incorrectExample = e
                break
        else:
            incorrectExample = e
            break
    
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
tree = FindOptModelStr(C, 10)
if(tree != None):
    print("final")
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    
    tree.test_decision_tree( C, CFeatures)
