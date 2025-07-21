from .node import Node

class Tree:
    """
    Class tree will provide a tree as well as utility functions.
    """
    def __init__(self, typePrecedence, type, registry, evaluate, get_type, get_type_on_next_keyword, fromInterpreter,toInterpreter, isTranslate:bool, safeExpressionList:list) -> None:
        self.tableauTypePrecedence = typePrecedence
        self.tableauType = type
        self.registry:dict = registry
        self.fromInterpreter = fromInterpreter
        self.toInterpreter = toInterpreter
        # self.evaluate = evaluate
        self.get_type = get_type
        self.get_type_on_next_keyword = get_type_on_next_keyword
        self.isTranslate = isTranslate
        self.safeExpressionList = safeExpressionList

    def createNode(self, data:list, original:str):
        """
        Utility function to create a node.
        """
        return Node(data, original, self.tableauType, self.get_type, self.get_type_on_next_keyword)

    def insert(self, parent:Node , data:list, original:str):
        """
        Insert function will insert expression as a node into tree.
        This function will also create child nodes dynamically.
        """
        #if tree is empty , return a root node
        if parent is None:
            parent = self.createNode(data, original)
            # self.evaluate(parent)
            self.insertChildren(parent)
        else:
            child = self.createNode(data, original)
            child.parent = parent
            parent.children.append(child)
            # self.evaluate(child)
            self.insertChildren(child)
        return parent
        
    def insertChildren(self, node:Node):
        """
        Recursively create child nodes and repeat insertion process
        """
        return self.fromInterpreter[0](node.type, self.insert, node)
                
    def search(self, node:Node, data:str):
        """
        Search function will search a node into tree.
        """
        # if root is None or root is the search data.
        if node is None or node.data == data:
            return node

        for node in node.children:
            self.search(node, data)

    def deleteNode(self,node:Node,data):
        """
        Delete function will delete a node into tree.
        Not complete , may need some more scenarion that we can handle
        Now it is handling only leaf.
        """

        # Check if tree is empty.
        if node is None:
            return None

        # searching key into BST.
        if node.data == data:
            del node
                
        else:
            for child in node.children:
                self.deleteNode(child, data)

    def traverseForExpression(self, node:Node, sub_col_ref, datatype:str, twb, tds):
        """
        traverse function will return one expression.
        """
        if node is not None:
            return self.toInterpreter[1](self.traverseForExpression, node,self.safeExpressionList ,sub_col_ref,self.isTranslate, self.registry, datatype, twb, tds)
        else:
            return "", 0

    def traverseInorder(self, node:Node):
        """
        traverse function will print all the node in the tree.
        """
        if node is not None:
            for child in node.children:
                self.traverseInorder(child)
                print(node.data)

    def traversePreorder(self, node:Node):
        """
        traverse function will print all the node in the tree.
        """
        if node is not None:
            print(f'node: {node.data} {node.keyword} {node.type}')
            for child in node.children:
                self.traversePreorder(child)

    def traversePostorder(self, root:Node):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            for child in root.children:
                self.traversePostorder(child)
            print(root.data)

    def shift_nodes(self, node:Node) -> None:
        """
        Shift nodes based on keyword
        """
        if node is not None:
            if node.keyword in self.registry.keys():
                # shift nodes with keyword
                return self.registry[node.keyword][0](node)

            elif node.type in self.registry.keys():
                # shift nodes with category
                return self.registry[node.type][0](node)

            else:
                # no shift required
                return
    
    def traverse_shift_nodes(self, node:Node) -> None:
        """
        Recursively shift nodes when tranversing down tree
        """
        if node is not None:
            self.shift_nodes(node)
            for child in node.children:
                self.traverse_shift_nodes(child)
