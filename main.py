C = [[1, 0, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 1, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [1, 0, 1, 0, 1],
     [0, 0, 0, 0, 1],
     [0, 0, 1, 0, 1],
     [0, 1, 0, 0, 1],
     [0, 1, 1, 0, 1],]
CFeatures = ["A", "B", "C", "D"]

def FindOptModelStr(C, s):
    return FindOptExtStr(C, s, None)

def FindOptExtStr(C, s, M):
    # search examples on tree and see if values are equal
    # return M

    node = M.root
    count = 0
    while(node.value == None ):
        count += 1
        node = node.child0

    



