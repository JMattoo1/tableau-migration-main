from ...expression import Node
import re
from ...error import ExpressionReformException, ExpressionTypeException, UnforseenCaseException

language = 'DAX'

reformCusImplementExpressions:set = set()

reformCusSafeExpressions:set = {
    # group
        '(',')', '{','}',
    # aggregation
        "SUM", "AVG", "MIN", "MAX", "COUNT",
    # logical
        "IF", "AND", "OR", "NOT",'SWITCH',
    # operators
        "+", "-", "*", "/", "%", "==", "=", ">", "<", ">=", "<=", "!=", "<>", "^",
    # number
        'ABS', 'ZN', 
    # detailLevel
        'FIXED',
    # mathTrig
        'CONVERT',
    # dateTime
        'DATEDIFF', 'DATEPART',
    # string
        'CONTAINS',
    # tableCal
        'TOTAL'
}

def struc_reform_if_to_switch(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    parameters = []
    req_reviews = 0

    for i, n in enumerate(node.children):
        parameter, req_review = traverse(n, sub_col_ref, datatype, twb, tds)
        parameters.append(parameter)
        req_reviews += req_review
    
    nullString = re.search(r'\[.*?\] = Null', parameters[0]) 
    if nullString:
        parameters[0] = f'ISBLANK( {re.sub(r" = [nNuUlL]+", "", parameters[0])} )'

    if node.keyword not in safeExpressionList:
        req_reviews += 1

    expression = f'SWITCH( TRUE(), {", ".join(parameters)} )'

    return expression, req_reviews

# def struc_reform_shift_case_to_switch(node:Node):
#     """
#     This function indicates no shifting of nodes in the tree
#     """
#     node.keyword = 'SWITCH'

def struc_reform_case_to_switch(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    parameters = []
    req_reviews = 0
    condition = ""
    node.keyword = 'SWITCH'

    for i, n in enumerate(node.children):
        parameter, req_review = traverse(n, sub_col_ref, datatype, twb, tds)
        if i == 0:
            condition = parameter

        else:
            if i % 2 != 0 and i != len(node.children) - 1:
                parameter = f'{condition} = {parameter}'

            parameters.append(parameter)
            req_reviews += req_review
    if node.keyword not in safeExpressionList:
        req_reviews += 1

    expression = f'SWITCH( TRUE(), {", ".join(parameters)} )'
    # expression = sub_col_ref(expression, twb, tds)
    return expression, req_reviews

def struc_reform_fixed_to_calculate(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    parameters = []
    req_reviews = 0
    for i, n in enumerate(node.children):
        parameter, req_review = traverse(n, sub_col_ref, datatype, twb, tds)
        parameters.append(parameter)
        req_reviews += req_review
    if node.keyword not in safeExpressionList:
        req_reviews += 1

    if parameters[0]:
        parameters[0] = parameters[0].split(',')
        result = []
        for p in parameters[0]:
            p = re.sub(r' ', '', p)
            p = sub_col_ref(p, twb, tds)

            if re.search(r'\'(.*?)\'',p):
                p = re.sub(r'\'(.*?)\'', f'\g<0>, \g<0>', p)
            else:
                p = f"'Table', 'Table'{p}"
            result.append(f'ALLEXCEPT( {p} )') 

        parameters[0] = result
    
    subExp = ", ".join(parameters[0])
    expressionlist = [parameters[1]]
    if subExp:
        expressionlist.append(subExp)
    expression = f'CALCULATE( {", ".join(expressionlist)} )'
    # expression = sub_col_ref(expression, twb, tds)
    return expression, req_reviews

def struc_reform_zn_to_if_isblank(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    req_reviews = 0

    if len(node.children) != 1:
        raise ValueError(f"Expected only 1 child node but given {len(node.children)} nodes")

    parameter, req_review = traverse(node.children[0], sub_col_ref, datatype, twb, tds)
    req_reviews += req_review

    if node.keyword not in safeExpressionList:
        req_reviews += 1

    expression = f'IF( ISBLANK( {parameter} ), 0, {parameter} )'
    # expression = sub_col_ref(expression, twb, tds)
    return expression, req_reviews

def struc_reform_shift_total_to_calculate(node: Node):
    """
    This function indicates shifting of nodes in the tree for total to calculate
    """
    if not node.children and len(node.children) == 1:
        raise ExpressionReformException(f'Expect exact one child but given {len(node.children)} node(s) for reform shift {node.type} {node.keyword}')
    
    child = node.children[0]

    if not child.children and len(child.children) == 1:
        raise ExpressionReformException(f'Expect exact one child one but given {len(child.children)} node(s) for {child.type} {child.keyword} and parent {node.type} {node.keyword}')
    
    node.children += child.children

def struc_reform_total_to_calculate(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):

    if len(node.children) != 2:
        raise ExpressionReformException(f'Expect exact two child but given {len(node.children)} node(s) for reform {node.type} {node.keyword}')
    
    filterVal = node.children[1]

    # if filterVal.type != 'exp': 
    #     raise ExpressionTypeException(f'Expect type exp but child (filter value) given type {filterVal.type} for reform {node.type} {node.keyword}')

    if filterVal.data:
        filterVal = " ".join(filterVal.data)
        filterVal = re.sub(r' ', '', filterVal)
        filterVal = sub_col_ref(filterVal, twb, tds)
        searchResult = re.search(r'\'(.*?)\'', filterVal)
        if not searchResult:
            raise UnforseenCaseException('Table reference not found')
        filterVal = searchResult[0]
    else:
        raise UnforseenCaseException('Table reference not found')

    parameter, req_review = traverse(node.children[0], sub_col_ref, datatype, twb, tds)

    expression = f'CALCULATE( {parameter}, ALL( {filterVal} ) )'

    return expression, req_review

def struc_reform_index_to_rankx(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')
