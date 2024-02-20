import dt
import config

def FindOptModelStr(C, s):
    return FindOptExtStr(C, s, None)

def FindOptExtStr(C, s, M):
    # search examples on tree and see if values are equal
    # return M

    incorrectExample = None
    countExamples = len(C)
    countCorrectExamples = 0
    for e in C:
        n = M.root
        while(n.value == None ):
            for f in CFeatures:
                index = 0
                if f == eLeaf.feature:
                    break

            if e[index] == 0:
                n = n.child0
            else:
                n = n.child1
        
        if n.value == e[-1]:
            countCurrentExamples += 1
        else:
            incorrectExample = e
    
    if countCurrentExamples == countExamples:
        return M
    
    node = M.root
    count = 1
    while(node.value == None ):
        count += 1
        node = node.child0
    count += 1
    while count >= s:
        return None
    






