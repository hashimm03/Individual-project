from dt import TreeNode, DecisionTree, FindStrictExtStr
from config import C, CFeatures

def FindOptModelStr(C, s):
    return FindOptExtStr(C, s, None)

def FindOptExtStr(C, s, M):
    # search examples on tree and see if values are equal
    # return M

    incorrectExample = None
    countExamples = len(C)
    countCorrectExamples = 0
    for e in C:
        if(M != None):
            n = M.root
            while(n.value == None ):
                index = 0
                for f in CFeatures:
                    if f == n.feature:
                        break
                    index += 1

                if e[index] == 0:
                    n = n.child0
                else:
                    n = n.child1
        
            if n.value == e[-1]:
                countCorrectExamples += 1
            else:
                incorrectExample = e
        else:
            incorrectExample = e
            break
    
    if(countCorrectExamples == countExamples):
        return M
    if(M == None):
        count = 0
    else:
        count = M.countNodes()
    if(count >= s):
        return None
    
    X = FindStrictExtStr(C, M, incorrectExample)
    
    B = None
    for tree in X:
        #tree.PrintTree()
        #input()
        if(tree.countNodes() <= s):
            A = FindOptExtStr(C, s, tree)
            if(A != None and (B == None or B.countNodes() > A.countNodes())):
                B = A
    return B
    
tree = FindOptModelStr(C, 10)
if(tree != None):
    print("final")
    tree.PrintTree()
    print(tree.countNodes(), " nodes")
    

    






