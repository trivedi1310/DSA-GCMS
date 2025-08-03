from node import Node

def comp_1(node_1, node_2):
    c1 = node_1.data.capacity
    c2 = node_2.data.capacity
    if c1 != c2:
        return -1 if c1 < c2 else 1
    return (node_1.data.bin_id > node_2.data.bin_id) - (node_1.data.bin_id < node_2.data.bin_id)

def comp_2(node_1, node_2):
    c1 = node_1.data.capacity
    c2 = node_2.data.capacity
    if c1 != c2:
        return -1 if c1 < c2 else 1
    return  (node_1.data.bin_id < node_2.data.bin_id) - (node_1.data.bin_id > node_2.data.bin_id)

def comp_3(node_1, node_2):
    id1 = node_1.data.bin_id
    id2 = node_2.data.bin_id
    if id1 != id2:
        return -1 if id1 < id2 else 1
    return 0


def comp_o(node_1, node_2):
    id1 = node_1.data.object_id
    id2 = node_2.data.object_id
    return (id1 > id2) - (id1 < id2)



class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.comparator = compare_function
    
    def height(self, node):
        if not node:
            return -1
        return node.height

    def rright(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    def rleft(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def add(self, value):
        new_node = Node(value) 
        self.root = self.insert(self.root, new_node)
        self.size += 1

    def insert(self, root, new_node):
        if root is None:
            root=new_node
            return root


        comparison = self.comparator(new_node, root)
        if comparison < 0:
            root.left = self.insert(root.left, new_node)
        elif comparison > 0:
            root.right = self.insert(root.right, new_node)
        else:
            return root
        
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.balancing(root)

    def balancing(self, node):
        balance = self.balance(node)
        
        if balance > 1:
            if self.balance(node.left) < 0:
                node.left = self.rleft(node.left)
            return self.rright(node)

        if balance < -1:
            if self.balance(node.right) > 0:
                node.right = self.rright(node.right)
            return self.rleft(node)
        
        return node

    

    def min_node(self, node):
        if node is None or node.left is None:
            return node
        return self.min_node(node.left)

    def delete(self, node, value):
        if not node:
            return node 

        comparison = self.comparator(Node(value), node)
        if comparison < 0:
            node.left = self.delete(node.left, value)
        elif comparison > 0:
            node.right = self.delete(node.right, value)
        else:
            if node.left is None:
                return node.right  
            elif node.right is None:
                return node.left  

            temp = self.min_node(node.right)
            node.data = temp.data  
            node.right = self.delete(node.right, temp.data) 

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        if balance > 1: 
            if self.balance(node.left) < 0: 
                node.left = self.rleft(node.left)
            return self.rright(node) 
        if balance < -1:  
            if self.balance(node.right) > 0:  
                node.right = self.rright(node.right)
            return self.rleft(node)  

        return node
    
    def remove(self, value):
        self.root = self.delete(self.root, value)
        self.size -= 1

    def in_order_traversal(self, node):
        if not node:
            return []
        return self.in_order_traversal(node.left) + [node.data.object_id] + self.in_order_traversal(node.right)

    
    def binsearch(self,root,id):
        if (not root):
            return None

        if(root.data.bin_id > id):
            return self.binsearch(root.left,id)
        elif (root.data.bin_id < id):
            return self.binsearch(root.right,id)
        else:
            return root

    def objsearch(self,root,id):
        if (not root):
            return None

        if(root.data.object_id > id):
            return self.objsearch(root.left,id)
        elif (root.data.object_id < id):
            return self.objsearch(root.right,id)
        else:
            return root