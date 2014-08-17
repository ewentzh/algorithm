#!/usr/bin/python

class RbNode(object):
    '''
    this is the rb tree node
    '''
    Red = 1
    Black = 0
    def __init__(self,key,data=None):
        '''
         RBTree Init routine: by default, the color is 1, it means red node.
        '''
        self.color = self.Red
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.data = data

    def __str__(self):
        return "key="+str(self.key)+",color="+str(self.color)

    def uncle(self):
        if self.parent is not None:
            if self.parent == self.parent.left:
                return self.parent.right
            else:
                return self.parent.left
        return None
        
class RbTree(object):
    def __init__(self):
        self.root = None

    def intert_node(self,root,node):
        pass

    def ll_rotate(self,node_x):
        '''
        left -> left rotate:
             O                      O
            / \                    / \ 
           X   O                  Y   O
          / \   \    ==>         / \   \ 
         O   Y  ...             X   R  ...
            / \                / \ 
           L   R              O   L
        '''

        node_y = node_x.right

        node_x.right = node_y.left
        if node_y.left is not None:
            node_y.left.parent = node_y
        node_y.parent = node_x.parent
        node_y.left = node_x
        if node_x.parent is None:
            self.root = node_y
        elif node_x.parent.left == node_x:
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y
        node_x.parent = node_y

    def rr_rotate(self,node_x):
        '''
        right -> right rotate:
             O                           O
            / \                         / \ 
           O   X                       O   Y
          /   / \      ==>            /   / \ 
         O   Y   O                   O   L   X
            / \                             / \ 
           L   R                           R   O
        '''
        node_y = node_x.left

        node_x.left = node_y.right
        if node_y.right is not None:
            node_y.right.parent = node_x
        node_y.right = node_x
        node_y.parent = node_x.parent

        if node_x.parent is None:
            self.root = node_y
        elif node_x.parent.left == node_x: 
            ## node_x is left child
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y
        node_x.parent = node_y

    def re_color_delete(self,node,parent):
        while node != self.root and (node is None or node.color == RbNode.Black):
            if node == parent.left:
                # node is left child
                w = parent.right
                if w.color == RbNode.Red:
                    w.color = RbNode.Black
                    parent.color = RbNode.Red
                    self.ll_rotate(parent)
                    w = parent.right
                if (w.left is None or w.left.color == RbNode.Black) and \
                       (w.right is None or w.right.color == RbNode.Black):
                    w.color = RbNode.Red
                    node = parent
                    parent = node.parent
                else:
                    if w.right is None or w.right.color == RbNode.Black:
                        if w.left is not None:
                            w.left.color = RbNode.Black
                        w.color = RbNode.Red
                        self.rr_rotate(w)
                        w = parent.right
                    w.color = parent.color
                    parent.color = RbNode.Black
                    if w.right is not None:
                        w.right.color = RbNode.Black
                    self.ll_rotate(parent)
                    node = self.root
                    break
            else:
                # node is right child.
                w = parent.left
                if w.color == RbNode.Red:
                    w.color = RbNode.Black
                    parent.color = RbNode.Red
                    self.rr_rotate(parent)
                    w = parent.left
                if (w.left is None or w.left.color == RbNode.Black) and \
                        ( w.right is None or w.left.color == RbNode.Balck):
                    w.color = RbNode.Red
                    node = parent
                    parent = node.parent
                else:
                    if w.left is None or w.left.color == RbNode.Black:
                        if w.right is not None:
                            w.right.color = RbNode.Red
                        w.color = RbNode.Red
                        self.ll_rotate(w)
                        w = parent.left
                    w.color = parent.color
                    parent.color = RbNode.Black
                    if w.left is not None:
                        w.left.color = RbNode.Black
                    self.rr_rotate(parent)
                    node = self.root
                    break
            if self.root is not None:
                self.root.color = RbNode.Black

    def re_color(self,node):
        '''
        re-color the rbtree.
          case 1:  if insert root node,just mark node as black. [done in insert, not in this function].
          case 2:  if parent is black. node is red, no impact, no action.
          case 3:  parent is red.  
        '''
        while node.parent is not None and node.parent.color == RbNode.Red:
            if node.parent.parent is not None and node.parent == node.parent.parent.left:   
                # parent is a left child.
                node_y = node.parent.parent.right
                if node_y is not None and node_y.color == RbNode.Red:                         # case 1.
                    # parent->left is Red.
                    # action:
                    #   mark parent, uncle to Black.
                    #   mark gradeparent Red.
                    #   set node to gradeparent.
                    node.parent.color = node_y.color = RbNode.Black
                    node.parent.parent.color = RbNode.Red
                    node = node.parent.parent
                elif node == node.parent.right:
                    # parent->left is Black.
                    # action:
                    #   set node <- parent.
                    #   ll-rotate
                    node = node.parent
                    self.ll_rotate(node)
                else:
                    node.parent.color = RbNode.Black
                    node.parent.parent.color = RbNode.Red
                    self.rr_rotate(node.parent.parent)
            elif node.parent.parent is not None and node.parent.parent.right == node.parent:
                node_y = node.parent.parent.left
                if node_y is not None and node_y.color == RbNode.Red:
                    # parent->left is Red.
                    node.parent.color = node_y.color = RbNode.Black
                    node.parent.parent.color = RbNode.Red
                    node = node.parent.parent
                elif node == node.parent.left:
                    node = node.parent
                    self.rr_rotate(node)
                else:
                    node.parent.color = RbNode.Black
                    node.parent.parent.color = RbNode.Red
                    self.ll_rotate(node.parent.parent)
            else:
                self.root.color = RbNode.Black
                break

    def insert(self,node):
        pos = None
        tmp = self.root
        while tmp is not None:
            pos = tmp
            if tmp.key > node.key:
                tmp = tmp.left
            elif tmp.key < node.key:
                tmp = tmp.right
            else:
                raise  "Key has Exist in the RBTree."
        if pos is None:
            self.root = node
            node.color = RbNode.Black
            return
        else:
            if pos.key < node.key:
                pos.right = node
            elif pos.key > node.key:
                pos.left = node
            else:
                raise "Key has exist in the RBTree."
        node.parent = pos
        self.re_color(node)


    def delete_node(self,node):
        def tree_successor(r):
            y = None
            if r.right is not None:
                # find the min in the r.right:
                y=r.right
                while y is not None and y.left is not None:
                    y = y.left
                return y
            y = node.parent
            while y is not None and y.right == r:
                r = y
                y = y.parent
            return y
        child = None
        parent = None
        if node.left is None:
            child = node.right
        elif node.right is None:
            child = node.left
        else:
            old = node
            node = tree_successor(node)
            #update the old's parent.
            if old.parent is not None:
                if old.parent.left == old:
                    old.parent.left = node
                else:
                    old.parent.right = node
            else:
                self.root = node
            # delete node here!!
            child = node.right
            parent = node.parent
            color = node.color
            if parent == old:
                #only one child.
                parent = node
            else:
                if child is not None:
                    child.parent = parent
                parent.left = child
                node.right = old.right
                old.right.parent = node

            node.left = old.left
            node.color = old.color
            old.left.parent = node
            node.parent = old.parent
            #node.key,old.key = old.key,node.key
            #node.data,old.data = old.data,node.data

            if color == RbNode.Black:
                self.re_color_delete(child,parent)
            return node

        parent = node.parent
        if child is not None:
            child.parent = parent
        if parent is not None:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child
        if node.color == RbNode.Black:
            self.re_color_delete(child,parent)

        return node


    def delete(self,key):
        pos = self.root
        while pos is not None:
            if pos.key == key:
                break
            elif pos.key > key:
                pos = pos.left
            else:
                pos = pos.right
        if pos is None:
            return
        return self.delete_node(pos)

    def traval(self):
        '''
        middle-traval
        '''
        def _tr(r):
            if r is None:
                return
            _tr(r.left)
            print r
            _tr(r.right)
        _tr(self.root)

    def hight(self):
        def h(r):
            if r == None:
                return 0
            left=h(r.left)
            right=h(r.right)
            if left >= right:
                return left+1
            else:
                return right+1
        return h(self.root)
    def count(self):
        def _c(r):
            if r is None:
                return 0
            return _c(r.left) + _c(r.right) +1
        return _c(self.root)
    def _ch(self,r):
        if r == None:
            return 0
        
        lColor = self.bh(r.left)
        rColor = self.bh(r.right)
        if lColor != rColor:
            print "Not Equal: lColor=" + str(lColor) + ",rColor="+str(rColor)
            print r
            
        self._ch(r.left)
        self._ch(r.right)


    def check(self):
        self._ch(self.root)
    def bh(self,r):
        rc=0
        if r is None:
            return 0
        if r.color is RbNode.Black:
            rc=1
        lc=self.bh(r.left)
        rrc = self.bh(r.right)
        if lc>=rrc:
            return lc+rc
        else:
            return rrc+rc
 
    def blackHight(self):
       return self.bh(self.root)

if __name__ == "__main__":
    root = RbTree()
    for i in (1,4,12,2,86,456,23,0,51,95):
        node = RbNode(i)
        root.insert(node)
    print "count is %d"% root.count()
    print "hight is %d"% root.hight()
    #root.traval()
    print root.root
    print str(root.root.left)+"  "+str(root.root.right)
    print str(root.root.right.left)+"  "+str(root.root.right.right)
    
    print "=========================="
    root.check()
    print root.blackHight()
    print "=========================="
    root.delete(86)
    root.delete(456)
    root.delete(23)
    root.delete(51)
    node = RbNode(85)
    root.insert(node)
    root.check()
    print "count is %d"% root.count()
    print "hight is %d"% root.hight()
    root.traval()
