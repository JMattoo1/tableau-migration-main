from itertools import chain
from ..language import *
from .breakdown import *
from .reform import *
from .utility import *
from ...error import ExpressionTypeException, CorrespondingPairNotFoundException, InbalancedPairFoundException

# Duplicated function
# MAX, MIN
# ZN
# DATEPARSE

_type = {
    "group": ["{","}", "(", ")"],
    # Types below are retrieved from: https://help.tableau.com/current/pro/desktop/en-us/functions.htm
    "aggregation": [
        "SUM", "AVG", "MIN", "MAX", "COUNT", 
        "MEDIAN", "ATTR","COUNTD", "COLLECT", "CORR",
        "COVAR", "COVARP", "PERCENTILE", "STDEV", "STDEVP",
        "VAR", "VARP"
    ],
    "dateTime": [
        "DATE", "DATEPART", "DATETRUNC", "TODAY", "NOW", 
        "DATEDIFF","DATEADD", "DATENAME", "DATEPARSE", "DAY",
        "ISDATE", "MAKEDATE", "MAKEDATETIME", "MAKETIME", "MAX",
        "MIN", "MONTH", "NOW", "QUARTER", "WEEK",
        "YEAR", "ISOQUARTER", "ISOWEEK", "ISOYEAR", "ISOWEEKDAY"
    ],
    "logical": [
        "IF", "AND", "OR", "NOT", "CASE", 
        "IN", "ELSE", "ELSEIF", "END", "IF",
        "IFNULL", "IIF", "ISDATE", "ISNULL", "MAX",
        "MIN", "THEN", "WHEN", 
        "ZN"
    ],
    "string":[
        'LEFT', 'RIGHT', 'UPPER', 'LOWER', 'TRIM',
        'ASCII', 'CHAR', 'CONTAINS', 'ENDSWITH', 'FIND',
        'FINDNTH', 'LEN', 'LTRIM', 'MAX', 'MID', 
        'MIN', 'PROPER', 'REPLACE', 'RTRIM', 'SPACE',
        'SPLIT', 'STARTSWITH'
    ], 
    "tableCal": [
        'WINDOW_SUM', 'RUNNING_SUM', 'TOTAL', 'RANK_DENSE', 'INDEX', 
        'WINDOW_MAX', 'WINDOW_AVG', 'FIRST', 'LAST', 'LOOKUP',
        'MODEL_EXTENSION_BOOL', 'MODEL_EXTENSION_INT', 'MODEL_EXTENSION_REAL', 'MODEL_EXTENSION_STRING', 'MODEL_PERCENTILE',
        'MODEL_QUANTILE', 'PREVIOUS_VALUE', 'RANK', 'RANK_MODIFIED', 'RANK_PERCENTILE',
        'RANK_UNIQUE', 'RUNNING_AVG', 'RUNNING_COUNT', 'RUNNING_MAX', 'RUNNING_MIN',
        'SIZE', 'SCRIPT_BOOL', 'SCRIPT_INT', 'SCRIPT_REAL', 'SCRIPT_STR',
        'WINDOW_CORR', 'WINDOW_COUNT', 'WINDOW_COVAR', 'WINDOW_COVARP', 'WINDOW_MEDIAN',
        'WINDOW_MIN', 'WINDOW_PERCENTILE', 'WINDOW_STDEV', 'WINDOW_STDEVP', 'WINDOW_VAR',
        'WINDOW_VARP'
    ], 
    "passThro": [
        # RAWSQL
        'RAWSQL_BOOL', 'RAWSQL_DATE', 'RAWSQL_DATETIME', 'RAWSQL_INT', 'RAWSQL_REAL',
        'RAWSQL_SPATIAL', 'RAWSQL_STR', 'RAWSQLAGG_BOOL', 'RAWSQLAGG_DATE', 'RAWSQLAGG_DATETIME',
        'RAWSQLAGG_INT', 'RAWSQLAGG_REAL', 'RAWSQLAGG_STR'
    ],
    "tableJoin": ['JOIN', 'BLEND', 'UNION'],
    "trend": ['FORECAST', 'TRENDLINE'],
    "number": [
        'ABS', 'ACOS', 'ASIN', 'ATAN', 'ATAN2',
        'CEILING', 'COS', 'COT', 'DEGREES', 'DIV',
        'EXP', 'FLOOR', 'HEXBINX', 'HEXBINY', 'LN',
        'LOG', 'MAX', 'MIN', 'PI', 'POWER',
        'RADIANS', 'ROUND', 'SIGN', 'SIN', 'SQRT',
        'SQUARE', 'TAN', 
        # 'ZN'
    ], 
    "detailLevel": ['FIXED', 'INCLUDE', 'EXCLUDE'],
    "operators": [
        "+", "-", "*", "/", "%", 
        "==", "=", ">", "<", ">=", 
        "<=", "!=", "<>", "^"
    ],
    "user": [
        'FULLNAME', 'ISFULLNAME', 'ISMEMBEROF', 'ISUSERNAME', 'USERDOMAIN',
        'USERNAME', 'USERATTRIBUTE', 'USERATTRIBUTEINCLUDES'
    ],
    "spatial": [
        'AREA', 'BUFFER', 'DISTANCE', 'INTERSECTS', 'MAKELINE',
        'MAKEPOINT'
    ],
    "typeConv": [
        'DATE', 'DATETIME', 'DATEPARSE', 'FLOAT', 'INT', 
        'STR'
    ],
    "additional": [
        # regular expressions
        'REGEXP_REPLACE', 'REGEXP_MATCH', 'REGEXP_EXTRACT', 'REGECP_EXTRACT_NTH',
        # hadoop hive
        'GET_JSON_OBJECT', 'PARSE_URL', 'PARSE_URL_QUERY', 'XPATH_BOOLEAN', 'XPATH_DOUBLE',
        'XPATH_FLOAT', 'XPATH_INT', 'XPATH_LONG', 'XPATH_SHORT', 'XPATH_STRING',
        # bigquery
        'DOMAIN', 'GROUP_CONCAT', 'HOST', 'LOG2', 'LTRIM_THIS', 
        'RTRIM_THIS', 'TIMESTAMP_TO_USEC', 'USEC_TO_TIMESTAMP', 'TLD'
    ]
}

_pair = {
    'END' : ['IF','CASE'],
    ')' : ['('],
    '}': ['{']
}

_typePrecedence = { 
    0: list(chain.from_iterable([_type.get(x) for x in ["group","detailLevel"]])),
    1: list(chain.from_iterable([_type.get(x) for x in ["logical","operators","aggregation", "dateTime", "tableCal", "tableJoin", "string", "trend"]]))
}

breakdownRegistry = {
    'logical': struc_breakdown_logical,
    'aggregation': struc_breakdown_aggregation,
    'group': struc_breakdown_group,
    'operators': struc_breakdown_operators,
    'number': struc_breakdown_number,
    'detailLevel': struc_breakdown_detailLevel,
    'exp': struc_breakdown_skip,
    'tableCal': struc_breakdown_tableCal,
    'typeConv': struc_breakdown_typeConv,
    'string': struc_breakdown_string,
    'user': struc_breakdown_user,
    'dateTime': struc_breakdown_dateTime,
    'undefined': struc_breakdown_skip
}

reformRegistry = {}

class Tableau(Language):
    """
    Class Tableau
    """
    _null = 'NULL'

    def __init__(self) -> None:
        self._type = _type
        self._typePrecedence = _typePrecedence
        self._pair = _pair
        self.implementedExpressions['break'] = breakImplementExpressions 
        self.implementedExpressions['reform'] = reformImplementExpressions
        self.safeExpressions['break'] = breakSafeExpressions 
        self.safeExpressions['reform'] = reformSafeExpressions
        super().__init__()
        
    def evaluate(self,node: Node):
        pass
        # match node.type:
        #     case 'logical' | 'tableCal' | 'aggregation' | 'group' | 'dateTime':
        #         # node is either a group, logical, aggregation or table calculation statement
        #         if node.keyword == "IF":
        #             # if statement
        #             patterns = ["IF","ELSEIF", "ELSE","THEN", "END"]
        #             patterns = find_patterns_used(patterns, node.data)
        #             pair = {'END' : 'IF'}
        #             open = "IF"
        #             close = "END"
        #         elif node.keyword == "CASE":
        #             # case statement
        #             patterns = ["CASE","WHEN","THEN", "ELSE","END"]
        #             patterns = find_patterns_used(patterns, node.data)
        #             pair = {'END' : 'CASE'}
        #             open = "CASE"
        #             close = "END"
        #         elif self.is_group(node):
        #             # group statement
        #             patterns = _type["group"]
        #             pair = {')' : '(', "}": "{"}
        #             open = node.keyword
        #             close = {v: k for k, v in pair.items()}[node.keyword]                
        #         else:
        #             # any other logical, aggregation, dateTime or table calculation statement
        #             patterns = ["(", ")"]
        #             pair = {')' : '(', "}": "{"}
        #             open = "("
        #             close = ")"

        #         if self.is_group(node):
        #             size = 2
        #         elif self.is_logical(node):
        #             if "IF" in patterns:
        #                 ifCount = node.data.count("IF")
        #                 elifCount = node.data.count("ELSEIF")
        #                 elseCount = node.data.count("ELSE")
        #                 size = ifCount * 3 + elifCount * 2 + elseCount
                        
        #                 # remove invalid 'ELSE' from 'CASE'
        #                 if 'CASE' in node.data:
        #                     for x in node.data.count('CASE'):
        #                         pass

        #             elif "CASE" in patterns:
        #                 caseCount = node.data.count("CASE")
        #                 whenCount = node.data.count("WHEN")
        #                 elseCount = node.data.count("ELSE")
        #                 size = caseCount * 2 + whenCount * 2 + elseCount                

        #                 # remove invalid 'ELSE' from 'IF'
        #                 if 'IF' in node.data:
        #                     for x in node.data.count('CASE'):
        #                         pass

        #             else:
        #                 size = len(patterns)
        #         else:
        #             size = len(patterns)


        #         positions, isBalanced = find_pattern_indices(patterns, node.data, size)

        #         # no or inbalanced set
        #         if not isBalanced:
        #             raise InbalancedPairFoundException(f'Inbalanced opening-closing pair {[open,close]} for {node.keyword} {node.type} size {size}')
        #             # raise InbalancedPairFoundException(f'Inbalanced opening-closing pair {[open,close]} for {node.data} parenthesisPos {positions} size {size}')
                
        #         closePos = find_corresponding_closing_index(positions,open, close, node.data, 0, pair)

        #         if not closePos:
        #             # Unable to find ending of the statement
        #             raise CorrespondingPairNotFoundException(f'Cannot find corresponding opening-closing pair {[open, close]} for {node.type} {node.keyword}')
        #             # raise OpenClosePairException(f'Cannot find corresponding opening-closing pair {[open, close]} for {node.data}')
                
        #         elif positions[closePos] == (len(node.data) - 1):
        #             # Valid for type and keyword identified
        #             return
        #         else:
        #             # Invalid for type and keyword identified
        #             start = positions[closePos]
        #             return self.get_type_on_next(node, self._typePrecedence, self._type,start)
                    
        #     case 'string':
        #         pass
        #     case 'tableJoin':
        #         pass
        #     case 'number':
        #         pass
        #     case 'statistical':
        #         pass
        #     case 'detailLevel':
        #         pass
        #     case 'operators':
        #         pass
        #     case 'exp':
        #         # node is a literal expression
        #         return self.get_type_on_next(node, self._typePrecedence, self._type)
            
        #     case 'trend':
        #         pass
        #     case _:
        #         return self.undefined_exp_tableau(node, )

    # def undefined_exp_tableau(self,node:Node):
    #     """
    #     Utility function for undefined tableau expression
    #     """
    #     if node.type not in _implementExpressions.keys() or node.keyword not in _implementExpressions[node.type]:
    #         node.type, node.keyword = "undefined", None
    #     return
    
    def get_type(self, data:list[str], tableauType: dict):
        """
        Utility function for identifying type of an expression
        """
        if data is not None:
            # get all keywords across all layers
            counts = {}
            indices = []
            keywords = list(chain.from_iterable([self._type.get(x) for x in self._type.keys()]))
            for i, v in enumerate(data):
                if v.upper() in keywords:
                    data[i] = v.upper()
                    counts.update({v.upper(): data.count(v)})
                    indices.append(i)

            # find all keywords in layer 1
            positions = []
            positions = get_outer_most_position_of_functions(indices, positions,data,0)
            outestKeyword:dict[str,list] = {}
            for i in positions:
                if data[i] not in outestKeyword.keys():
                    outestKeyword[data[i]] = [i]
                else:
                    outestKeyword[data[i]].append(i)

            # find the only keyword in layer 1
            keys = outestKeyword.keys()

            if positions:
                if any(k in ["AND", "OR"] for k in keys):
                    # special handling for functions taking left-right, logical
                    for key in keys:
                        if key in ["AND", "OR"]:
                            return 'logical', key, outestKeyword[key][0]


                elif any(k in self._type['operators'] for k in keys):
                    # special handling for functions taking left-right, operators
                    operators = [
                        # level 1
                        ["==", "=", ">", "<", ">=","<=", "!=", "<>"],
                        # level 2
                        ['*','/','%'],
                        # level 3
                        ["+", "-", "^"]
                    ]
                    for o in operators:
                        if any(k in o for k in keys):
                            for key in keys:
                                if key in o:
                                    return 'operators', key, outestKeyword[key][0]

                else:
                    for type in self._type.keys():
                        key = data[positions[0]]
                        if key in self._type[type]:
                            return type, key, positions[0]
                    raise ExpressionTypeException(f'Keywords "{", ".join(keys)}" are found but type is undetermined')
            elif re.search(r'#[0-9/]+#', data[0]):
                return 'dateTime', data[0], 0
            else:
                return "exp", None, 0

            return "exp", "exp"

        else:
            return None, None
            
    def get_type_on_next(self, node: Node, tableauTypePrecedence: dict, tableauType: dict, start: int = 0) -> None:
        """
        Utility function for identifying type of an expression on nexy keyword
        """
        if start + 1 < len(node.data) and node.data[start + 1] in tableauType.keys():
            node.type, node.keyword, node.position = node.get_type(node.data[start+1],tableauType)
            return
        else:
            node.type, node.keyword = "exp", None
            return


        # for order in tableauTypePrecedence:
        #     # skip group type
        #     if order > 0:
        #         for i, v in enumerate(node.data):
        #             if i > start:
        #                 if v in tableauTypePrecedence[order]:
        #                     node.type, node.keyword = node.get_type(v,tableauType)
        #                     return
        # node.type, node.keyword = "exp", None
        # return

    def _create_breakdown_structure(self):
        super()._create_breakdown_structure()
        return self.structure_breakdown.update(breakdownRegistry)

    def _create_reform_structure(self):
        super()._create_reform_structure()
        return self.structure_reform.update(reformRegistry)
    
    def is_group(self, node:Node):
        return node.type == 'group'
    
    def is_aggregation(self, node:Node):
        return node.type == 'aggregation'

    def is_dateTime(self, node:Node):
        return node.type == 'dateTime'

    def is_logical(self, node:Node):
        return node.type == 'logical'

    def is_string(self, node:Node):
        return node.type == 'string'

    def is_tableCal(self, node:Node):
        return node.type == 'tableCal'

    def is_tableJoin(self, node:Node):
        return node.type == 'tableJoin'

    def is_number(self, node:Node):
        return node.type == 'number'

    def is_statistical(self, node:Node):
        return node.type == 'statistical'

    def is_trend(self, node:Node):
        return node.type == 'trend'

    def is_detailLevel(self, node:Node):
        return node.type == 'detailLevel'

    def is_operators(self, node:Node):
        return node.type == 'operators'
