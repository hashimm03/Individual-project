domain = ""
if domain == "b":
    from dt import TreeNode, DecisionTree, FindStrictExtStr
    from config import C, CFeatures
else:
    from dt_integer import TreeNode, DecisionTree, FindStrictExtStr
    from config import C, CFeatures, orderFeatures

import time
countTrees = 0

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
        global countTrees 
        if(tree.countNodes() <= s):
            global countTrees
            countTrees += 1
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
        global countTrees
        countTrees += 1
        if(tree.countNodes() <= s):
            global start_time
            current_time = time.perf_counter()
            if (current_time - start_time) > 1000:
                return None
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
    
    # Find a reasonable upper bound for `s`, e.g., total number of nodes in a fully expanded tree

    low, high = 1, 2*len(C) - 1
    
    best_tree = None
    while low <= high:
        print(low)
        print(high)
        mid = (low + high) // 2
        print(mid)
        tree = FindOptModelStr_BinarySearch(C, mid)
        global start_time
        current_time = time.perf_counter()
        if (current_time - start_time) > 1000:
            print("Timing out due to long execution")
            print(f"Low: {low}, High: {high}")
            return None
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
    max = 2*len(C) + 1
    while tree is None and s<max:
        s += 1
        #
        tree = FindOptModelStr(C, s)

    return tree

# usage
# Start the timer

start_time = time.perf_counter()

# Call the function to find the minimal tree
tree = FindOptModelStr(C, 5)

# Stop the timer
end_time = time.perf_counter()

# Calculate the elapsed time
runtime = (end_time - start_time) * 1000

# Output the runtime
print(f"Runtime: {runtime} milliseconds")
print(f"Number of Trees Created: {countTrees} trees")

if(tree != None):
    print(f"Minimal Decision Tree: {tree.countNodes()} nodes")

"""
def run_with_timeout(C):
    global low, high, countTrees
    global start_time
    
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(FindMinimalTree_BinarySearch, C)
            tree = future.result(timeout=1000)  # Timeout set for 1000 seconds
            if tree:
                end_time = time.perf_counter()
                runtime = (end_time - start_time) * 100
                print(f"Minimal Decision Tree: {tree.countNodes()} nodes")
                print(f"Runtime: {runtime:.2f} milliseconds")
    except TimeoutError:
        print("Function timed out!")
        print(f"Low: {low}, High: {high}")
        # Here you handle the printing when a timeout occurs
    finally:
        print(f"Number of Trees Cre ted: {countTrees}")


tree = FindMinimalTree(C)
if(tree != None):
    tree.PrintTree()
    tree.TestDeisionTree(C)
"""
