from ..language import *
from .breakdown import *
from .reform import *

_type = {
    'group': ['(',')'],
    'aggregation': [],
    'dateTime': [],
    'filter': [],
    'financial': [],
    'information': [
        'CONTAINSSTRING',
    ],
    'logical': [],
    'mathTrig': [],
    'other': [],
    'parentChild': [],
    'relationship': [],
    'statiscal': [],
    'tableManipulation': [],
    'text': [],
    'timeInt': []
}

_typePrecedence = {}

breakdownRegistry = {}

reformRegistry = {}

class Dax(Language):
    """
    Class Dax
    """
    _null = "BLANK()"

    def __init__(self) -> None:
        self._type = _type
        self._typePrecedence = _typePrecedence
        self.implementedExpressions['break'] = breakImplementExpressions 
        self.implementedExpressions['reform'] = reformImplementExpressions
        self.safeExpressions['break'] = breakSafeExpressions 
        self.safeExpressions['reform'] = reformSafeExpressions
        super().__init__()
    
    def evaluate(self,node: Node):
        return super().evaluate()

    def get_type(self, keyword, tableauType: dict):
        return super().get_type(keyword, tableauType)
    
    def get_type_on_next(self, node: Node, tableauTypePrecedence: dict, tableauType: dict, start: int = 0) -> None:
        return super().get_type_on_next(node, tableauTypePrecedence, tableauType, start)

    def _create_breakdown_structure(self):
        super()._create_breakdown_structure()
        return self.structure_breakdown.update(breakdownRegistry)

    def _create_reform_structure(self):
        super()._create_reform_structure()
        return self.structure_reform.update(reformRegistry)
