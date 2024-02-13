class DecisionTreeNode:
    def __init__(self, attribute=None, value=None, true_branch=None, false_branch=None, result=None):
        self.attribute = attribute  # Attribute to split on
        self.value = value          # Value of the attribute to split on
        self.true_branch = true_branch  # Subtree for when the attribute is true
        self.false_branch = false_branch  # Subtree for when the attribute is false
        self.result = result        # Result if it's a leaf node

class DecisionTree:
    def __init__(self, root=None):
        self.root = root  # Root node of the decision tree

    def predict(self, instance):
        return self._predict(instance, self.root)

    def _predict(self, instance, node):
        if node.result is not None:
            return node.result

        if instance[node.attribute] == node.value:
            return self._predict(instance, node.true_branch)
        else:
            return self._predict(instance, node.false_branch)