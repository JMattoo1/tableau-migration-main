__type__ = ["group", "exp", "logical", "aggregation", "detailLevel", "tableCal", "operators"]

class Node:
    """
    Class Node
    """
    def __init__(self, data:list[str], original:str, tableauType:dict, get_type,get_type_on_next_keyword,children:list=None, context = None) -> None:
        self.data = data
        self.get_type = get_type
        self.original = original
        self.context = context
        self.get_type_on_next_keyword = get_type_on_next_keyword
        if self.data:
            self.type, self.keyword, self.position = self.get_type(data, tableauType)
        else:
            self.type, self.keyword, self.position = None, None, None
        self.parent = None
        self.children:list[Node] = children or []
