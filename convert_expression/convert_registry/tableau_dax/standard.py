from ...expression import Node
from ...error import UnforseenCaseException, ExpressionBreakdownException, ExpressionReformException
import re

language = 'DAX'

reformStdImplementExpressions = {
    # aggregation
    'AVERAGE'
}


reformStdSafeExpressions = {
    # group
    '(',')', '{','}',
    # aggregation
    "SUM", "AVERAGE", "MIN", "MAX", "COUNT",
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

# null value for Dax
null = 'BLANK()'

def struc_reform_no_shift_node(node:Node):
    """
    This function indicates no shifting of nodes in the tree
    """

def struc_reform_if_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    """
    Shift node from Tableau If's structure to structure equivalent in Dax
    """
    raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')

def struc_reform_aggregation_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    parameters = ""
    req_reviews = 0

    for child in node.children:
        parameter, req_review = traverse(child, sub_col_ref, datatype, twb, tds)
        parameters += parameter
        req_reviews += req_review
        
    if node.keyword not in safeExpressionList:
        req_reviews += 1

    if node.keyword == 'AVG':
        node.keyword = 'AVERAGE'

    expression = f'{node.keyword}( {parameters} )'
    # expression = sub_col_ref(expression, twb, tds)
    return expression, req_reviews
    
def struc_reform_undefined_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    expression = " ".join(node.data)
    # expression = sub_col_ref(expression, twb, tds)
    return expression, 1

def struc_reform_expression_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    expression = " ".join(node.data)
    # expression = sub_col_ref(expression, twb, tds)

    # convert true/false to equivalent in DAX
    if expression.lower() in ['true','false']:
        expression = f'{expression.upper()}()'
        
    return expression, 0

def struc_reform_logical_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):

    parameters = []
    req_reviews = 0

    for child in node.children:
        parameter, req_review = traverse(child, sub_col_ref, datatype, twb, tds)
        parameters.append(parameter)
        req_reviews += req_review

    if node.keyword == "IF":
        # IF statement

        if node.keyword not in safeExpressionList:
            req_reviews += 1

        expression = f'SWITCH( TRUE(), {", ".join(parameters)})'

    elif node.keyword in ['AND', 'OR']:
        # "AND", "OR"
        toOperators = {
            'AND': '&&',
            'OR': '||'
        }
        if node.keyword not in safeExpressionList:
            req_reviews += 1

        if node.keyword not in toOperators.keys():
            raise ExpressionReformException(f'Found unknown keyword {node.keyword}')
        
        parameters.insert(1, toOperators[node.keyword])

        expression = f'{" ".join(parameters)}'

    elif node.keyword in ['NOT']:
        # "NOT"
        
        if node.keyword not in safeExpressionList:
            req_reviews += 1

        expression = f'{node.keyword}( {", ".join(parameters)} )'

    elif node.keyword in ['ISNULL']:

        expression = f'ISBLANK( {", ".join(parameters)} )'

    elif node.keyword in ['IFNULL']:

        if len(parameters) != 2:
            raise ExpressionBreakdownException(f'Expect exact two child but given {len(node.children)} node(s) for reform {node.type} {node.keyword}')

        condition = f'ISBLANK( {parameters[0]} )'

        expression = f'IF( NOT( {condition} ), {parameters[0]}, {parameters[1]} )'

    else:
        raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')
    
    # expression = sub_col_ref(expression, twb, tds)

    return expression, req_reviews

def struc_reform_operators_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    operands = []
    req_reviews = 0
    for child in node.children:
        operand, req_review = traverse(child, sub_col_ref, datatype, twb, tds)
        operands.append(operand)
        req_reviews += req_review

    # change to equivalent operator in DAX
    if node.keyword == '!=':
        node.keyword = '<>'
    elif node.keyword == '+' and datatype == 'string':
        node.keyword = '&'

    # verify for safe expression
    if node.keyword not in safeExpressionList:
        req_reviews += 1
    
    # change to function in DAX
    if node.keyword =='%':
        expression =f'MOD( {", ".join(operands)} )'
    elif node.keyword == '/':
        expression =f'DIVIDE( {", ".join(operands)} )'
    elif node.keyword == '-':
        match len(operands):
            case 1:
                expression = f'{node.keyword}{operands[0]}'
            case 2:
                operands.insert(1, node.keyword)
                expression = " ".join(operands)
            case _:
                raise UnforseenCaseException(f'{language}-Reform for {node.keyword} {node.type}')
            
    else:
        operands.insert(1, node.keyword)
        expression = " ".join(operands)
    # expression = sub_col_ref(expression, twb, tds)
    return expression, req_reviews

def struc_reform_group_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    if node.keyword == '(':
        expression, review =traverse(node.children[0], sub_col_ref, datatype, twb, tds)
        return f'( {expression} )', review
    else:
        return traverse(node.children[0], sub_col_ref, datatype, twb, tds)

def struc_reform_tableCal_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')

def struc_reform_typeConv_to_convert_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    if node.keyword in ['INT']:
        dataType = 'DOUBLE'
    
    elif node.keyword in ['STR']:
        dataType = 'STRING'

    else:
        raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')
    

    parameters = ""
    req_reviews = 0

    for child in node.children:
        parameter, req_review = traverse(child, sub_col_ref, datatype, twb, tds)
        parameters += parameter
        req_reviews += req_review

    node.type = 'information'
    
    if node.keyword in ['INT']:
        node.keyword = 'ROUNDDOWN'
        expression = f'ROUNDDOWN( CONVERT( {parameters}, {dataType} ), 0 )'
    else:
        node.keyword = 'CONVERT'
        expression = f'{node.keyword}( {parameters}, {dataType} )'

    if node.keyword not in safeExpressionList:
        req_reviews += 1

    # expression = sub_col_ref(expression, twb, tds)

    return expression, req_reviews
    
def struc_reform_string_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    if node.keyword in ['CONTAINS']:

        parameters = []
        req_reviews = 0

        for child in node.children:
            parameter, req_review = traverse(child, sub_col_ref, datatype, twb, tds)
            parameters.append(parameter)
            req_reviews += req_review
            
        if node.keyword not in safeExpressionList:
            req_reviews += 1

        expression = f'CONTAINSSTRING( {", ".join(parameters)} )'
        # expression = sub_col_ref(expression, twb, tds)

        return expression, req_reviews

    else:
        raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')

def struc_reform_dateTime_exp(traverse, node:Node, safeExpressionList:list, sub_col_ref, datatype, twb, tds):
    
    if node.keyword in ['DATEPART']:
        if len(node.children) == 2:
            req_reviews = 0

            parameter, req_review = traverse(node.children[1], sub_col_ref, datatype, twb, tds)
            req_reviews += req_review

            if node.keyword not in safeExpressionList:
                req_reviews += 1

            interval = "".join(node.children[0].data)
            interval = sub_col_ref(interval, twb, tds)


            match interval:
                case "'second'" | '"second"':
                    interval = 'SECOND'
                case "'minute'" | '"minute"':
                    interval = 'MINUTE'
                case "'hour'" | '"hour"':
                    interval = 'HOUR'
                case "'day'" | '"day"':
                    interval = 'DAY'
                case "'week'" | '"week"':
                    interval = 'WEEKNUM'
                case "'weekday'" | '"weekday"':
                    interval = 'WEEKDAY'
                case "'month'" | '"month"':
                    interval = 'MONTH'
                case "'quarter'" | '"quarter"':
                    interval = 'QUARTER'
                case "'year'" | '"year"':
                    interval = 'YEAR'
                case _:
                    raise UnforseenCaseException(f'{language}-Reform for {node.keyword} {node.type} experience an unforseen case {node.children[0].data} {interval}')

            expression = f'{interval}( {parameter} )'
            # expression = sub_col_ref(expression, twb, tds)

            # if interval in ["'year'", '"year"']:
            #     expression = f'YEAR( {parameter} )'
            # elif interval in ["'month'", '"month"']:
            #     expression = f'MONTH( {parameter} )'
            # elif interval in ["'day'", '"day"']:
            #     expression = f'DAY( {parameter} )'
            # else:
            #     raise UnforseenCaseException(f'{language}-Reform for {node.keyword} {node.type} experience an unforseen case {node.children[0].data} {interval}')


            return expression, req_reviews

        else:
            raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')

    elif node.keyword in ['DATEDIFF']:
        if len(node.children) == 3:
            parameters = []
            req_reviews = 0

            interval = "".join(node.children[0].data)
            interval = sub_col_ref(interval, twb, tds) 

            match interval:
                case "'second'" | '"second"':
                    interval = 'SECOND'
                case "'minute'" | '"minute"':
                    interval = 'MINUTE'
                case "'hour'" | '"hour"':
                    interval = 'HOUR'
                case "'day'" | '"day"':
                    interval = 'DAY'
                case "'week'" | '"week"':
                    interval = 'WEEK'
                # Removed
                # case "'weekday'" | '"weekday"':
                #     interval = 'WEEKDAY'
                case "'month'" | '"month"':
                    interval = 'MONTH'
                case "'quarter'" | '"quarter"':
                    interval = 'QUARTER'
                case "'year'" | '"year"':
                    interval = 'YEAR'
                case _:
                    raise UnforseenCaseException(f'{language}-Reform for {node.keyword} {node.type} experience an unforseen case {node.children[0].data} {interval}')

            for index in range(1, len(node.children)):
                parameter, req_review = traverse(node.children[index], sub_col_ref, datatype, twb, tds)
                parameters.append(parameter)
                req_reviews += req_review

            if node.keyword not in safeExpressionList:
                req_reviews += 1

            expression = f'{node.keyword}( {", ".join(parameters)}, {interval} )'
            # expression = sub_col_ref(expression, twb, tds)

            return expression, req_reviews

        else:
            raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')

    elif node.keyword in ['DATEPARSE']:
        if len(node.children) == 2:
            parameters = ""
            req_reviews = 0

            parameter, req_review = traverse(node.children[0], sub_col_ref, datatype, twb, tds)
            value, req_review2 = traverse(node.children[1], sub_col_ref, datatype, twb, tds)

            req_reviews += req_review + req_review2
                
            if node.keyword not in safeExpressionList:
                req_reviews += 1

            expression = f'FORMAT( {value}, {parameter} )'
            # expression = sub_col_ref(expression, twb, tds)

            return expression, req_reviews
        
        else:

            raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')
    elif node.keyword in ['YEAR']:
        parameters = ""
        req_reviews = 0

        parameter, req_review = traverse(node.children[0], sub_col_ref, datatype, twb, tds)
        req_reviews += req_review
            
        if node.keyword not in safeExpressionList:
            req_reviews += 1

        expression = f'YEAR( {parameter} )'
        # expression = sub_col_ref(expression, twb, tds)

        return expression, req_reviews

    elif node.keyword in ['TODAY']:
        parameters = ""
        req_reviews = 0
            
        if node.keyword not in safeExpressionList:
            req_reviews += 1

        expression = f'{node.keyword}()'

        return expression, req_reviews
    
    elif re.search(r'#[0-9/]+#', node.keyword):
        string = re.search(r'#[0-9/]+#', node.keyword).group()
        string = re.sub(r'#',"",string).strip()

        if string:
            from datetime import datetime
            year = string.split('/')[-1]
            if int(year) >= 100:
                date = datetime.strptime(string, '%m/%d/%Y')
            else:
                date = datetime.strptime(string, '%m/%d/%y')

            expression = f'DATE( {date.year}, {date.month}, {date.day} )'

            return expression, 0
        else:
            raise ExpressionReformException(f'Expect exact one date but given {string} for reform {node.type} {node.keyword}')


    
    else:
        raise NotImplementedError(f'{language}-Reform for {node.keyword} {node.type} is not implemented')
