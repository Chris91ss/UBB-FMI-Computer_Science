class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.preIndex = 0
        self.postIndex = 0

    def build_tree(self, in_order, order, in_start, in_end, is_preorder=True):
        if in_start > in_end:
            return None

        if is_preorder:
            tNode = Node(order[self.preIndex])
            self.preIndex += 1
        else:
            tNode = Node(order[self.postIndex])
            self.postIndex -= 1

        if in_start == in_end:
            return tNode

        inIndex = search(in_order, in_start, in_end, tNode.data)

        if is_preorder:
            tNode.left = self.build_tree(in_order, order, in_start, inIndex - 1, is_preorder)
            tNode.right = self.build_tree(in_order, order, inIndex + 1, in_end, is_preorder)
        else:
            tNode.right = self.build_tree(in_order, order, inIndex + 1, in_end, is_preorder)
            tNode.left = self.build_tree(in_order, order, in_start, inIndex - 1, is_preorder)

        return tNode


# UTILITY FUNCTIONS
# Function to find index of value in arr[start...end]
# The function assumes that value is present in inOrder[]

def search(arr, start, end, value):
    for i in range(start, end + 1):
        if arr[i] == value:
            return i


def print_inorder(node):
    if node is None:
        return

    # first recur on left child
    print_inorder(node.left)

    # then print the data of node
    print(node.data),

    # now recur on right child
    print_inorder(node.right)


def print_preorder(node):
    if node is None:
        return

    # first print the data of node
    print(node.data),

    # then recur on left child
    print_preorder(node.left)

    # now recur on right child
    print_preorder(node.right)


def print_postorder(node):
    if node is None:
        return

    # first recur on left child
    print_postorder(node.left)

    # then recur on right child
    print_postorder(node.right)

    # now print the data of node
    print(node.data)


def run_app():
    inOrder = ['D', 'B', 'E', 'A', 'F', 'C']
    preOrder = ['A', 'B', 'D', 'E', 'C', 'F']
    postOrder = ['D', 'E', 'B', 'F', 'C', 'A']

    tree = BinaryTree()
    tree.preIndex = 0
    root = tree.build_tree(inOrder, preOrder, 0, len(inOrder) - 1, is_preorder=True)

    print("Tree constructed from preorder and inorder")
    print("Inorder traversal of the constructed tree is")
    print_inorder(root)

    print("Preorder traversal of the constructed tree is")
    print_preorder(root)

    print("Postorder traversal of the constructed tree is")
    print_postorder(root)

    tree.postIndex = len(inOrder) - 1
    root = tree.build_tree(inOrder, postOrder, 0, len(inOrder) - 1, is_preorder=False)

    print("Tree constructed from postorder and inorder")
    print("Inorder traversal of the constructed tree is")
    print_inorder(root)

    print("Preorder traversal of the constructed tree is")
    print_preorder(root)

    print("Postorder traversal of the constructed tree is")
    print_postorder(root)

# We cannot reconstruct a tree from postorder and preorder traversals
# Example:
# Tree 1: Root node ‘A’ with left child ‘B’ and right child ‘C’.
# Tree 2: Root node ‘A’ with left child ‘C’ and right child ‘B’.
# Both of these trees have the same preorder traversal (A, B, C) and the same post-order traversal (B, C, A),
