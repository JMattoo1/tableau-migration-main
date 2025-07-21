from abc import ABC, abstractmethod
from ..expression import Node
from itertools import chain
import traceback
from .utility import expressionKey

class Language(ABC):
    _type = {}
    _typePrecedence = {}
    structure_breakdown: dict[str] = {}
    structure_reform: dict[str] = {}
    implementedExpressions: dict[str,set] = dict.fromkeys(expressionKey, set())
    safeExpressions: dict[str,set] = dict.fromkeys(expressionKey, set())

    def __init__(self) -> None:
        self._create_breakdown_structure()
        self._create_reform_structure()

    @property
    def variables(self):
        """
        Return function types and their order's precedence of a language
        """
        return self._type, self._typePrecedence
    
    @property
    def expressions(self):
        """
        Return lists that contain keywords which every keyword is referencing to a function and that are implemeted and safely used
        """
        return self.implementedExpressions, self.safeExpressions
    
    @property
    def utilities(self):
        """
        Return methods for a language that are used to evaluate and determines type of a statement
        """
        return self.evaluate, self.get_type, self.get_type_on_next
    
    @property
    def interpreter(self) ->tuple:
        """
        Return methods that either breakdown a statement or reform a statement from tree-node structure 
        """
        return self.breakdown, self.reform
    
    def breakdown(self, keyword:str, insert, node:Node):
        """
        Breakdown a statement into a tree-node structure
        """
        try:
            if keyword in self.structure_breakdown.keys() and self.structure_breakdown[keyword]:
                return self.structure_breakdown[keyword](insert, node)
            else:
                raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} "from" language is not implemented')
        except NotImplementedError:
            return self.structure_breakdown['undefined'](insert, node)
        
    def reform(self, traverse, node:Node, safeExpressionList,sub_col_ref,isTranslate:bool=False, registry:dict = None, datatype:str = None, twb:str = None, tds: str = None):
        """
        Reform a statement from a tree-node structure
        """
        try:
            if isTranslate:
                if not registry:
                    raise ValueError('Expected dictionary mapping to translating function')
                else:
                    reformR = registry
            else:
                raise NotImplementedError('Reform for same languages "to" and "from" is not implemeted')

            if not node.type and not node.keyword:
                return '' , 0
            elif node.keyword and node.keyword in reformR.keys():
                return reformR[node.keyword][1](traverse,node, safeExpressionList, sub_col_ref, datatype, twb, tds)
            elif node.type and node.type in reformR.keys():
                return reformR[node.type][1](traverse,node, safeExpressionList,sub_col_ref, datatype, twb, tds)
            elif node.keyword or node.type:
                return reformR['undefined'][1](traverse,node, safeExpressionList, sub_col_ref, datatype, twb, tds)
            else:
                raise ValueError(f'Expected either type or keyword but given {node.type} {node.keyword}')
        except NotImplementedError:
            return reformR['undefined'][1](traverse,node, safeExpressionList, sub_col_ref, datatype, twb, tds)

    @abstractmethod
    def evaluate(self,node: Node):
        """
        Evaluate and correct if node's type is falsely identified
        """
        pass

    @abstractmethod
    def get_type(self,keyword, tableauType:dict) -> tuple[str,str,int]:
        """
        Utility function to define type for expression in this node
        """
        pass

    @abstractmethod
    def get_type_on_next(self,node:Node, tableauTypePrecedence:dict,tableauType:dict,start:int = 0) -> None:
        """
        Utility function to define type for expression based on next keyword in this node
        """
        pass

    def _create_breakdown_structure(self):
        """
        Initialize dictionary that stores type-function for breaking down a statement
        """
        self.structure_breakdown = dict.fromkeys(self._type.keys())
    
    def _create_reform_structure(self):
        """
        Initialize dictionary that stores keyword/type-function for reforming a statement
        """
        keywords = list(chain.from_iterable([self._type.get(x) for x in self._type.keys()]))
        self.structure_reform = dict.fromkeys(keywords)