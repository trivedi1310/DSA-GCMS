from bin import Bin
from avl import *
from object import Object, Color
from exceptions import NoBinFoundException

def blue(root, size):
    if(root==None):
        return None
    curr=root
    ans=root
    while(curr!=None):
        if(curr.data.capacity>=size):
            ans=curr
            curr=curr.left
        else:
            curr=curr.right

    if(ans.data.capacity>=size):
        return ans
    else:
        return None

            
def yellow(root, size):
    # # Base case: if the root is None, return None
    # curr=root
    # mincap=0
    # while curr is not None:
    #     mincap=max(mincap,curr.data.capacity)
    #     curr=curr.right
    # curr=root
    # while curr is not None:
    #     if curr.data.capacity>=size:
    #         mincap=min(mincap,curr.data.capacity)
    #         curr=curr.left
    #     else:
    #         curr=curr.right
    # maxid=0
    # st=root
    # while st is not None:
    #     if st.data.capacity>mincap:
    #         st=st.left
    #     elif st.data.capacity<mincap:
    #         st=st.right
    #     else:
    #         maxid=max(maxid,st.data.bin_id)
    #         st=st.right
    # return GCMS().treeid.binsearch(root,maxid)
    if root==None:
        return None
    x=blue(root,size)
    if not x:
        return x
    curr=root
    while(curr!=None):
        if(curr.data.capacity>x.data.capacity):
            curr=curr.left
        else:
            if(x.data.capacity==curr.data.capacity and x.data.bin_id<curr.data.bin_id):
                x=curr
            curr=curr.right
    if(x.data.capacity>=size):
        return x
    else:
        return None
        

def green(root,size):
    if not root:
        return root
    x=root
    while x.right!=None:
        x=x.right
    if x.data.capacity>=size:
        return x
    else:
        return None


def red(root, size):
    if not root:
        return root
    curr=root
    x=green(root,size)
    if not x:
        return x
    while(curr):
        if(curr.data.capacity<x.data.capacity):
            curr=curr.right
        else:
            if(x.data.bin_id>curr.data.bin_id):
                x=curr
            curr=curr.left
    if(x.data.capacity>=size):
        return x
    else:
        return None


class GCMS:
    def __init__(self):
        self.tree1=AVLTree(comp_1)  
        self.treeid=AVLTree(comp_3) 
        self.objs=AVLTree(comp_o)

    def add_bin(self, bin_id, capacity):
        bin=Bin(bin_id,capacity)
        self.tree1.add(bin)
        self.treeid.add(bin)

    # def add_object(self, object_id, size, color):
    #     o=Object(object_id,size,color)
    #     if color==1:
    #         o.baap=blue(self.tree1.root,size)
    #     elif color==2:
    #         o.baap=yellow(self.tree1.root,size)
    #     elif color==3:
    #         o.baap=red(self.tree1.root,size)
    #     else:
    #         o.baap=green(self.tree1.root,size)
        
    #     self.objs.add(o)
    #     if(o.baap==None or o.baap.data.capacity<size):
    #         raise NoBinFoundException
    #     b=o.baap.data
    #     self.tree1.remove(b)
    #     b.binobjs.add(o)
    #     b.capacity-=o.size
    #     self.tree1.add(b)
    #     print("sent into",b.bin_id,b.capacity)

    def add_object(self, object_id, size, color):
        o = Object(object_id, size, color)
        # Assign the correct bin to the object based on color
        if color == Color.BLUE:
            best = blue(self.tree1.root,size)
            if best is None or best.data.capacity < size:
                raise NoBinFoundException
            # print("blue",best.data.capacity,best.data.bin_id)
        elif color == Color.YELLOW:
            best = yellow(self.tree1.root,size)
            if best is None or best.data.capacity < size:
                raise NoBinFoundException
            # print("yellow",best.data.capacity,best.data.bin_id)
        elif color == Color.RED:
            best = red(self.tree1.root,size)
            if best is None or best.data.capacity < size:
                raise NoBinFoundException
            # print("red",best.data.capacity,best.data.bin_id)
        else:
            best = green(self.tree1.root,size)
            if best is None or best.data.capacity < size:
                raise NoBinFoundException
            # print("green",best.data.capacity,best.data.bin_id)

        # Add the object to the AVL tree containing objects
        # If no suitable bin was found or the bin doesn't have enough capacity, raise an exception
        

        o.baap=best.data  # Get the bin itself
        b=o.baap
        
        self.objs.add(o)
        # Remove the bin from tree1 for modification
        self.tree1.remove(b)
        b.binobjs.add(o)
        b.capacity -= o.size
        self.tree1.add(b)

        # b_=Bin(b.bin_id,b.capacity)
        # self.treeid.remove(b_)
        # b_.binobjs=b.binobjs
        # b_.capacity = b.capacity
        # self.treeid.add(b_)

        # Output the result for debugging or feedback
        # print(object_id,"sent into", b.bin_id, b.capacity)
        # print("struct",self.tree1.root.data.capacity,self.tree1.root.data.bin_id)
        # if self.tree1.root.left:
        #     print("struct left",self.tree1.root.left.data.capacity,self.tree1.root.left.data.bin_id)
        # if self.tree1.root.right:
        #     print("struct rigft",self.tree1.root.right.data.capacity,self.tree1.root.right.data.bin_id)
        # if self.tree1.root.left.left:
        #     print("struct left left",self.tree1.root.left.left.data.capacity,self.tree1.root.left.left.data.bin_id)
        # if self.tree1.root.right.left:
        #     print("struct rigft left",self.tree1.root.right.left.data.capacity,self.tree1.root.right.left.data.bin_id)

        # if self.tree1.root.left.right:
        #     print("struct left right",self.tree1.root.left.right.data.capacity,self.tree1.root.left.right.data.bin_id)
        # if self.tree1.root.right.right:
        #     print("struct rigft right",self.tree1.root.right.right.data.capacity,self.tree1.root.right.right.data.bin_id)



    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        try:
            n=self.objs.objsearch(self.objs.root,object_id)
            x=n.data.size
            b=n.data.baap

            self.tree1.remove(b)
            b.binobjs.remove(n.data)
            b.capacity+=x
            self.tree1.add(b)

            self.objs.remove(n.data)
        except:
            pass

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        n=self.treeid.binsearch(self.treeid.root,bin_id)
        # print("me",n.data.capacity,n.data.bin_id)
        # if n.left!=None:
        #     print("left",n.left.data.capacity,n.left.data.bin_id)
        # if n.right!=None:
        #     print("right",n.right.data.capacity,n.right.data.bin_id)
        return (n.data.capacity, n.data.binobjs.in_order_traversal(n.data.binobjs.root))

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        try:
            n=self.objs.objsearch(self.objs.root,object_id)
            b=n.data.baap
            return b.bin_id
        except:
            pass
    