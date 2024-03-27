# Problem Set 4a
# Name: Abayo Joseph Desire
# Collaborators: Lily(Mentor)
# Time spent:

from tree import Node  # Imports the Node object used to construct trees

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree_1 = Node(9, Node(6), Node(3, Node(7), Node(8)))
tree_2 = Node(7, Node(13, Node(15, Node(4), Node(6)), Node(5)), Node(2, Node(9), Node(11)))
tree_3 = Node(4, Node(9, Node(14), Node(25)), Node(17, Node(1), Node(8, Node(11), Node(6))))

def find_tree_height(tree):
    '''
    Find the height of the given tree
    Input:
        tree: An element of type Node constructing a tree
    Output:
        The integer depth of the tree
    '''
    if tree.get_left_child() == None and tree.get_right_child() == None:
        return 0
    elif tree.get_left_child() != None and tree.get_right_child() != None:
        left_node = find_tree_height(tree.get_left_child())
        right_node=find_tree_height(tree.get_right_child())
        if left_node > right_node:
            return 1 + left_node
        else:
            return 1 + right_node
    elif tree.get_left_child() != None and tree.get_right_child() == None:
        return 1 + find_tree_height(tree.get_left_child())
    else:
        return 1 + find_tree_height(tree.get_right_child())

def is_heap(tree, compare_func):
    '''
    Determines if the tree is a max or min heap depending on compare_func
    Inputs:
        tree: An element of type Node constructing a tree compare_func:
              a function that compares the child node value to the parent node value

            i.e. compare_func(child_value,parent_value) for a max heap would return False
                 if child_value > parent_value and True otherwise

                 compare_func(child_value,parent_value) for a min meap would return False
                 if child_value < parent_value and True otherwise
    Output:
        True if the entire tree satisfies the compare_func function; False otherwise
    '''
    if tree.get_left_child() == None and tree.get_right_child() == None:
        return True
    else:
        left_val=tree.get_left_child()
        right_val=tree.get_right_child()
        if left_val == None:
            if compare_func(right_val.get_value(), tree.get_value()):
                return is_heap(right_val, compare_func)
            return False
        elif right_val == None:
            if compare_func(left_val.get_value(), tree.get_value()):
                return is_heap(left_val, compare_func)
            return False
        else:
            if compare_func(left_val.get_value(), tree.get_value()) and compare_func(right_val.get_value(), tree.get_value()):
                return is_heap(left_val, compare_func) and is_heap(right_val, compare_func)
            return False

if __name__ == '__main__':
    # # You can use this part for your own testing and debugging purposes.
    # # IMPORTANT: Do not erase the pass statement below if you do not add your own code
    # max heap comparator
    def compare_func_max(child_value, parent_value):
        if child_value > parent_value:
            return False
        return True

    # min heap comparator
    def compare_func_min(child_value, parent_value):
        if child_value < parent_value:
            return False
        return True
    print(is_heap(tree_1, compare_func_max))
