from ..language import *
from ...utility import *
from .utility import *
from ...error import InbalancedPairFoundException, ExpressionBreakdownException

language = 'Tableau'

breakImplementExpressions = {

    # group
    "{","}", "(", ")",
    
    # aggregation
    "SUM", "AVG", "MIN", "MAX", "COUNT", 
    # "MEDIAN", "ATTR","COUNTD", "COLLECT", "CORR",
    # "COVAR", "COVARP", "PERCENTILE", "STDEV", "STDEVP",
    # "VAR", "VARP",

    # dateTime
    "DATE", "DATEPART", "DATEDIFF",
    # "DATETRUNC", "TODAY", "NOW", 
    # "DATEADD", "DATENAME", "DATEPARSE", "DAY",
    # "ISDATE", "MAKEDATE", "MAKEDATETIME", "MAKETIME", "MAX",
    # "MIN", "MONTH", "NOW", "QUARTER", "WEEK",
    # "YEAR", "ISOQUARTER", "ISOWEEK", "ISOYEAR",

    # logical
    "IF", "AND", "OR", "NOT", "CASE",
    "ELSE", "ELSEIF", "END", "IFNULL", "ISNULL", 
    "THEN", "WHEN", "ZN",
    # "IN", "IIF", "ISDATE", "MAX", "MIN", 
    
    # string
    'LEFT', 'RIGHT', 'CONTAINS',
    # 'UPPER', 'LOWER', 'TRIM',
    # 'ASCII', 'CHAR', 'ENDSWITH', 'FIND',
    # 'FINDNTH', 'LEN', 'LTRIM', 'MAX', 'MID', 
    # 'MIN', 'PROPER', 'REPLACE', 'RTRIM', 'SPACE',
    # 'SPLIT', 'STARTSWITH',

    # tableCal
    'WINDOW_SUM', 'RUNNING_SUM', 'TOTAL', 'INDEX', 
    # 'RANK_DENSE', 
    # 'WINDOW_MAX', 'WINDOW_AVG', 'FIRST', 'LAST', 'LOOKUP',
    # 'MODEL_EXTENSION_BOOL', 'MODEL_EXTENSION_INT', 'MODEL_EXTENSION_REAL', 'MODEL_EXTENSION_STRING', 'MODEL_PERCENTILE',
    # 'MODEL_QUANTILE', 'PREVIOUS_VALUE', 'RANK', 'RANK_MODIFIED', 'RANK_PERCENTILE',
    # 'RANK_UNIQUE', 'RUNNING_AVG', 'RUNNING_COUNT', 'RUNNING_MAX', 'RUNNING_MIN',
    # 'SIZE', 'SCRIPT_BOOL', 'SCRIPT_INT', 'SCRIPT_REAL', 'SCRIPT_STR',
    # 'WINDOW_CORR', 'WINDOW_COUNT', 'WINDOW_COVAR', 'WINDOW_COVARP', 'WINDOW_MEDIAN',
    # 'WINDOW_MIN', 'WINDOW_PERCENTILE', 'WINDOW_STDEV', 'WINDOW_STDEVP', 'WINDOW_VAR',
    # 'WINDOW_VARP', 

    # passThro (RAWSQL)
    # 'RAWSQL_BOOL', 'RAWSQL_DATE', 'RAWSQL_DATETIME', 'RAWSQL_INT', 'RAWSQL_REAL',
    # 'RAWSQL_SPATIAL', 'RAWSQL_STR', 'RAWSQLAGG_BOOL', 'RAWSQLAGG_DATE', 'RAWSQLAGG_DATETIME',
    # 'RAWSQLAGG_INT', 'RAWSQLAGG_REAL', 'RAWSQLAGG_STR',

    # tableJoin 
    # 'JOIN', 'BLEND', 'UNION',


    # trend
    # 'FORECAST', 'TRENDLINE',

    # number
    'ABS', 
    # 'ACOS', 'ASIN', 'ATAN', 'ATAN2',
    # 'CEILING', 'COS', 'COT', 'DEGREES', 'DIV',
    # 'EXP', 'FLOOR', 'HEXBINX', 'HEXBINY', 'LN',
    # 'LOG', 'MAX', 'MIN', 'PI', 'POWER',
    # 'RADIANS', 'ROUND', 'SIGN', 'SIN', 'SQRT',
    # 'SQUARE', 'TAN', 
    # # 'ZN', 
    
    # detailLevel
    'FIXED', 
    # 'INCLUDE', 'EXCLUDE',

    # operators
    "+", "-", "*", "/", "%", 
    "==", "=", ">", "<", ">=",
    "<=", "!=", "<>", "^",

    # user
    # 'FULLNAME', 'ISFULLNAME', 'ISMEMBEROF', 'ISUSERNAME', 'USERDOMAIN',
    # 'USERNAME', 'USERATTRIBUTE', 'USERATTRIBUTEINCLUDES',

    # spatial
    # 'AREA', 'BUFFER', 'DISTANCE', 'INTERSECTS', 'MAKELINE',
    # 'MAKEPOINT',

    # typeConv
    'DATE', 'INT', 'STR',
    # 'DATETIME', 'DATEPARSE', 'FLOAT', 

    # additional
    # # regular expressions
    # 'REGEXP_REPLACE', 'REGEXP_MATCH', 'REGEXP_EXTRACT', 'REGECP_EXTRACT_NTH',
    # # hadoop hive
    # 'GET_JSON_OBJECT', 'PARSE_URL', 'PARSE_URL_QUERY', 'XPATH_BOOLEAN', 'XPATH_DOUBLE',
    # 'XPATH_FLOAT', 'XPATH_INT', 'XPATH_LONG', 'XPATH_SHORT', 'XPATH_STRING',
    # # bigquery
    # 'DOMAIN', 'GROUP_CONCAT', 'HOST', 'LOG2', 'LTRIM_THIS', 
    # 'RTRIM_THIS', 'TIMESTAMP_TO_USEC', 'USEC_TO_TIMESTAMP', 'TLD'
    
}

breakSafeExpressions = {

    # group
    "{","}", "(", ")",
    
    # aggregation
    "SUM", "AVG", "MIN", "MAX", "COUNT", 
    # "MEDIAN", "ATTR","COUNTD", "COLLECT", "CORR",
    # "COVAR", "COVARP", "PERCENTILE", "STDEV", "STDEVP",
    # "VAR", "VARP",

    # dateTime
    "DATE", "DATEPART", "DATEDIFF",
    # "DATETRUNC", "TODAY", "NOW", 
    # "DATEADD", "DATENAME", "DATEPARSE", "DAY",
    # "ISDATE", "MAKEDATE", "MAKEDATETIME", "MAKETIME", "MAX",
    # "MIN", "MONTH", "NOW", "QUARTER", "WEEK",
    # "YEAR", "ISOQUARTER", "ISOWEEK", "ISOYEAR",

    # logical
    "IF", "AND", "OR", "NOT", "CASE",
    "ELSE", "ELSEIF", "END", "IFNULL", "ISNULL", 
    "THEN", "WHEN", "ZN",
    # "IN", "IIF", "ISDATE", "MAX", "MIN", 
    
    # string
    'LEFT', 'RIGHT', 'CONTAINS',
    # 'UPPER', 'LOWER', 'TRIM',
    # 'ASCII', 'CHAR', 'ENDSWITH', 'FIND',
    # 'FINDNTH', 'LEN', 'LTRIM', 'MAX', 'MID', 
    # 'MIN', 'PROPER', 'REPLACE', 'RTRIM', 'SPACE',
    # 'SPLIT', 'STARTSWITH',

    # tableCal
    'WINDOW_SUM', 'RUNNING_SUM', 'TOTAL', 'INDEX', 
    # 'RANK_DENSE', 
    # 'WINDOW_MAX', 'WINDOW_AVG', 'FIRST', 'LAST', 'LOOKUP',
    # 'MODEL_EXTENSION_BOOL', 'MODEL_EXTENSION_INT', 'MODEL_EXTENSION_REAL', 'MODEL_EXTENSION_STRING', 'MODEL_PERCENTILE',
    # 'MODEL_QUANTILE', 'PREVIOUS_VALUE', 'RANK', 'RANK_MODIFIED', 'RANK_PERCENTILE',
    # 'RANK_UNIQUE', 'RUNNING_AVG', 'RUNNING_COUNT', 'RUNNING_MAX', 'RUNNING_MIN',
    # 'SIZE', 'SCRIPT_BOOL', 'SCRIPT_INT', 'SCRIPT_REAL', 'SCRIPT_STR',
    # 'WINDOW_CORR', 'WINDOW_COUNT', 'WINDOW_COVAR', 'WINDOW_COVARP', 'WINDOW_MEDIAN',
    # 'WINDOW_MIN', 'WINDOW_PERCENTILE', 'WINDOW_STDEV', 'WINDOW_STDEVP', 'WINDOW_VAR',
    # 'WINDOW_VARP', 

    # passThro (RAWSQL)
    # 'RAWSQL_BOOL', 'RAWSQL_DATE', 'RAWSQL_DATETIME', 'RAWSQL_INT', 'RAWSQL_REAL',
    # 'RAWSQL_SPATIAL', 'RAWSQL_STR', 'RAWSQLAGG_BOOL', 'RAWSQLAGG_DATE', 'RAWSQLAGG_DATETIME',
    # 'RAWSQLAGG_INT', 'RAWSQLAGG_REAL', 'RAWSQLAGG_STR',

    # tableJoin 
    # 'JOIN', 'BLEND', 'UNION',


    # trend
    # 'FORECAST', 'TRENDLINE',

    # number
    'ABS', 
    # 'ACOS', 'ASIN', 'ATAN', 'ATAN2',
    # 'CEILING', 'COS', 'COT', 'DEGREES', 'DIV',
    # 'EXP', 'FLOOR', 'HEXBINX', 'HEXBINY', 'LN',
    # 'LOG', 'MAX', 'MIN', 'PI', 'POWER',
    # 'RADIANS', 'ROUND', 'SIGN', 'SIN', 'SQRT',
    # 'SQUARE', 'TAN', 
    # # 'ZN', 
    
    # detailLevel
    'FIXED', 
    # 'INCLUDE', 'EXCLUDE',

    # operators
    "+", "-", "*", "/", "%", 
    "==", "=", ">", "<", ">=",
    "<=", "!=", "<>", "^",

    # user
    # 'FULLNAME', 'ISFULLNAME', 'ISMEMBEROF', 'ISUSERNAME', 'USERDOMAIN',
    # 'USERNAME', 'USERATTRIBUTE', 'USERATTRIBUTEINCLUDES',

    # spatial
    # 'AREA', 'BUFFER', 'DISTANCE', 'INTERSECTS', 'MAKELINE',
    # 'MAKEPOINT',

    # typeConv
    'DATE', 'INT', 'STR',
    # 'DATETIME', 'DATEPARSE', 'FLOAT', 

    # additional
    # # regular expressions
    # 'REGEXP_REPLACE', 'REGEXP_MATCH', 'REGEXP_EXTRACT', 'REGECP_EXTRACT_NTH',
    # # hadoop hive
    # 'GET_JSON_OBJECT', 'PARSE_URL', 'PARSE_URL_QUERY', 'XPATH_BOOLEAN', 'XPATH_DOUBLE',
    # 'XPATH_FLOAT', 'XPATH_INT', 'XPATH_LONG', 'XPATH_SHORT', 'XPATH_STRING',
    # # bigquery
    # 'DOMAIN', 'GROUP_CONCAT', 'HOST', 'LOG2', 'LTRIM_THIS', 
    # 'RTRIM_THIS', 'TIMESTAMP_TO_USEC', 'USEC_TO_TIMESTAMP', 'TLD'
    
}


def struc_breakdown_skip(insert, node:Node):
    """
    Breakdown is not required
    """
    pass

def __struc_breakdown_single_child(insert, node:Node):
    """
    Breakdown but only has one child
    """
    _, isBalanced = find_pattern_indices(["(",")"], node.data, 2)

    # inbalanced pair of parenthesis
    if not isBalanced:
        raise InbalancedPairFoundException(f'Inbalanced parenthesis found for {node.keyword} {node.type}')

    data = node.data[2:-1]
    insert(node, data, " ".join(data))

def __struc_breakdown_two_children(insert, node:Node):
    """
    Breakdown but only has two children
    """
    _, isBalanced = find_pattern_indices(["(",")"], node.data, 2)

    # inbalanced pair of parenthesis
    if not isBalanced:
        raise InbalancedPairFoundException(f'Inbalanced parenthesis found for {node.keyword} {node.type}')

    exp = node.data[2:-1]

    commaPos = [i for i, v in enumerate(exp) if v in [',', '(',')','{','}']]

    nestedPos = []
    stack = []
    for i,v in enumerate(commaPos):
        if exp[v] in ['(','{']:
            stack.append(i)
        elif exp[v] in [')','}']:
            start = stack.pop()
            end = i
            nestedPos.append((start, end))
        else:
            continue
    
    for s,e in reversed(nestedPos):
        commaPos = commaPos[:s] + commaPos[e+1:]
            

    if len(commaPos) != 1:
        raise ExpressionBreakdownException(f'Expected 2 parameters but found {"None" if not exp else len(commaPos) + 1 } {exp}')

    children = []
    firstChild, secondChild= [], []

    # first param
    firstChild = exp[:commaPos[0]]
    children.append(firstChild)
    # second param
    secondChild = exp[commaPos[0] + 1:]
    children.append(secondChild)
    
    for childData in children:
        insert(node, childData, " ".join(childData))    

def __struc_breakdown_three_or_more_children(insert, node:Node, number:int):
    """
    Breakdown but has three or more children
    """
    _, isBalanced = find_pattern_indices(["(",")"], node.data, 2)

    # inbalanced pair of parenthesis
    if not isBalanced:
        raise InbalancedPairFoundException(f'Inbalanced parenthesis found for {node.keyword} {node.type}')

    exp = node.data[2:-1]

    commaPos = [i for i, v in enumerate(exp) if v == ',']


    nestedPos = []
    stack = []
    for i,v in enumerate(commaPos):
        if exp[v] in ['(','{']:
            stack.append(i)
        elif exp[v] in [')','}']:
            start = stack.pop()
            end = i
            nestedPos.append((start, end))
        else:
            continue
    
    for s,e in reversed(nestedPos):
        commaPos = commaPos[:s] + commaPos[e+1:]


    if len(commaPos) != number - 1:
        raise ExpressionBreakdownException(f'Found {len(commaPos)} commas but expected only {number}')

    children = []

    for n in range(number):
        if n == 0:
            # first child
            children.append(exp[:commaPos[n]])
        elif n == number - 1:
            # last child
            children.append(exp[commaPos[n-1]+1:])
        else:
            # children between first and last
            children.append(exp[commaPos[n-1]+1:commaPos[n]])

    for childData in children:
        insert(node, childData, " ".join(childData))    


def struc_breakdown_logical(insert, node:Node):
    """
    Break an expression into structure of a logical statement
    """
    children = []

    if node.keyword in ["IF", 'CASE']:

        ifCount = node.data.count("IF")
        caseCount = node.data.count("CASE")
        elifCount = node.data.count("ELSEIF")
        elseCount = node.data.count("ELSE")
        whenCount = node.data.count("WHEN")
        thenCount = node.data.count("THEN")
        endCount = node.data.count('END')

        if 'IF' in node.data and 'CASE' in node.data:
            size = caseCount + whenCount + elseCount + endCount + ifCount + elifCount + thenCount
            patterns = ["IF","ELSEIF", "ELSE","THEN", "END" , "CASE","WHEN"]

        elif 'IF' in node.data:
            size = ifCount * 3 + elifCount * 2 + elseCount
            patterns = ["IF","ELSEIF", "ELSE","THEN", "END"]

        else:
            size = caseCount * 2 + whenCount * 2 + elseCount
            patterns = ["CASE","WHEN","THEN", "ELSE","END"]

        usedPatterns = find_patterns_used(patterns, node.data)

    elif node.keyword in ['AND', 'OR', 'NOT','ZN','ISNULL', 'IFNULL']:
        # "AND", "OR", "NOT"
        usedPatterns = [node.keyword]
        size = 1
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')
        # raise NotImplementedError(f'{language} for breakdown {node.keyword} or {node.type} is not implemented')

    positions, isBalanced = find_pattern_indices(usedPatterns, node.data, size)

    if node.keyword in ["IF", "CASE"]:
        if not isBalanced or not positions:
            newKeywords = [node.data[x] for x in positions]
            raise InbalancedPairFoundException(f'Inbalanced {node.keyword}-END pair {positions} {newKeywords}')
            # raise InbalancedPairFoundException(f'Inbalanced {node.keyword}-END pair for {node.data} size {size} parenthesisPos {positions}')
        # Add step to remove nested positions
        newPositions = []
        newPositions = get_outer_most_position_of_functions(positions, newPositions, node.data,0)
        # tempPositions = remove_nested_position_of_functions_with_same_closing(tempPositions, {closing:['CASE', 'IF']},closing,data)

        newPositions = remove_nested_position_of_functions_with_same_closing(positions, {'END':['CASE', 'IF']},'END',node.data)

        for l in range(len(newPositions)):
            if l == len(newPositions) - 1:
                children.append(node.data[newPositions[l]+1: -1])
            else:
                children.append(node.data[newPositions[l]+1: newPositions[l+1]])

    elif node.keyword in ['AND', 'OR', 'NOT']:
        if not positions:
            raise ValueError(f'Cannot find postion for {node.keyword} given {node.type}')
        
        positions = [i for i,v in enumerate(node.data) if v in ['(',')',node.keyword]]
        nestedPos = []
        stack = []
        for i, v in enumerate(positions):
            if node.data[v] == '(':
                stack.append(i)
            elif node.data[v] == ')':
                start = stack.pop()
                end = i
                nestedPos.append((start,end))
            else:
                continue

        for s, e in reversed(nestedPos):
            positions = positions[:s] + positions[e + 1:]

        left = node.data[:positions[0]]
        right:list = node.data[positions[0]:]
        right.remove(node.keyword)
        children.append(left)
        children.append(right)

    elif node.keyword in ['ZN','ISNULL']:
        return __struc_breakdown_single_child(insert,node)
    
    elif node.keyword in ['IFNULL']:
        return __struc_breakdown_two_children(insert,node)
    
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')
        # raise NotImplementedError(f'{language} for breakdown {node.keyword} or {node.type} is not implemented')
    for childData in children:
        if childData:
            insert(node, childData, " ".join(childData))

def struc_breakdown_aggregation(insert, node:Node):
    """
    Break an expression into structure of an aggregation statement
    """
    return __struc_breakdown_single_child(insert, node)

def struc_breakdown_group(insert, node:Node):
    """
    Break an expression into structure of an group statement
    """
    patterns = ["{","}", "(", ")"]
    _, isBalanced =find_pattern_indices(patterns, node.data, 2)

    # inbalanced pair of curly brackets
    if not isBalanced:
        raise InbalancedPairFoundException(f'Inbalanced curly brackets found for {node.keyword}')
        # raise InbalancedPairFoundException(f'Inbalanced curly brackets found for {node.data}')
    
    data = node.data[1:-1]
    insert(node, data, " ".join(data))

def struc_breakdown_operators(insert, node:Node):
    """
    Break an expression into structure of an operator statement
    """

    children = []
    left = node.data[:node.position]
    right:list = node.data[node.position:]
    right.remove(node.keyword)
    children.append(left)
    children.append(right)

    for childData in children:
        if childData:
            insert(node, childData, " ".join(childData))

def struc_breakdown_number(insert, node:Node):
    """
    Break an expression into structure of an number statement
    """
    if node.keyword in ['ABS']:
        patterns = ["(", ")"]
        _, isBalanced =find_pattern_indices(patterns, node.data, 2)

        # inbalanced pair of curly brackets
        if not isBalanced:
            raise InbalancedPairFoundException(f'Inbalanced curly brackets found for {node.keyword} {node.type}')
            # raise InbalancedPairFoundException(f'Inbalanced curly brackets found for {node.data}')
        data = node.data[1:]
        insert(node, data, " ".join(data))

    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')
    
def struc_breakdown_detailLevel(insert, node:Node):
    """
    Break an expression into structure of an detail level statement
    """
    if node.keyword == 'FIXED':
        exp = node.data[1:]
        if ':' in exp:
            semi_pos = exp.index(':')
        else:
            raise ExpressionBreakdownException(f'Language {language}: Expected ":" in {exp}')

        children = []
        left = exp[:semi_pos]
        left = [" ".join(left)]
        right:list = exp[semi_pos:]
        right.remove(':')
        children.append(left)
        children.append(right)

        for childData in children:
            insert(node, childData, " ".join(childData))
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')

def struc_breakdown_tableCal(insert, node:Node):
    """
    Break an expression into structure of a table calculation statement
    """
    if node.keyword in ['INDEX']:
        return struc_breakdown_skip(insert, node)
    
    elif node.keyword in ['TOTAL', 'RUNNING_SUM']:
        return __struc_breakdown_single_child(insert, node)
    
    elif node.keyword in ['WINDOW_SUM']:
        exp = node.data[2:-1]
        
        commaPos = [i for i, v in enumerate(exp) if v == ',']

        if not (not commaPos or len(commaPos) == 2):
            raise ExpressionBreakdownException(f'Expected 1 or 3 parameters but found {"None" if not exp else len(commaPos) + 1 }')

        children = []
        firstChild, secondChild, thirdChild = [], [], []

        if commaPos:
            firstChild = exp[:commaPos[0]]
            children.append(firstChild)
        else:
            children.append(exp)

        if len(commaPos) == 2:
            secondChild = exp[commaPos[0] + 1:commaPos[1]]
            children.append(secondChild)
            thirdChild = exp[commaPos[1] + 1:]
            children.append(thirdChild)
        
        for childData in children:
            insert(node, childData, " ".join(childData))
        
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')

def struc_breakdown_typeConv(insert, node:Node):
    """
    Break an expression into structure of a type converting statement
    """
    if node.keyword in ['INT','DATE','STR']:
        return __struc_breakdown_single_child(insert, node)
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')

def struc_breakdown_string(insert, node:Node):
    """
    Break an expression into structure of a type converting statement
    """
    if node.keyword in ['RIGHT','LEFT','CONTAINS']:
        return __struc_breakdown_two_children(insert, node)
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')

def struc_breakdown_user(insert, node:Node):
    """
    Break an expression into structure of a type converting statement
    """
    if node.keyword in ['ISMEMBEROF']:
        return __struc_breakdown_single_child(insert, node)
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')

def struc_breakdown_dateTime(insert, node:Node):
    """
    Break an expression into structure of a type converting statement
    """
    exp = node.data[2:-1]
    commaPos = [i for i, v in enumerate(exp) if v == ',']

    if node.keyword in ['DATEPARSE']:
        # 1/2 params
        if not len(commaPos) <= 1 or not len(commaPos) >= 0:
            raise ExpressionBreakdownException(f'Expected 1 or 2 parameters but found {"None" if not exp else len(commaPos) + 1 }')
        
        if len(commaPos) == 0:
            return __struc_breakdown_single_child(insert, node)
        else:
            return __struc_breakdown_two_children(insert, node)

    if node.keyword in ['DATEPART']:
        # 2/3 params
        if not (len(commaPos) == 1 or len(commaPos) == 2):
            raise ExpressionBreakdownException(f'Expected 1 or 2 parameters but found {"None" if not exp else len(commaPos) + 1 }')
        if len(commaPos) == 1:
            return __struc_breakdown_two_children(insert, node)
        else:
            return __struc_breakdown_three_or_more_children(insert, node, 3)
        
    elif node.keyword in ['DATEDIFF']:
        # 3/4 params
        if not (len(commaPos) == 2 or len(commaPos) == 3):
            raise ExpressionBreakdownException(f'Expected 3 or 4 parameters but found {"None" if not exp else len(commaPos) + 1 }')
        if len(commaPos) == 2:
            return __struc_breakdown_three_or_more_children(insert, node, 3)
        else:
            return __struc_breakdown_three_or_more_children(insert, node, 4)
        
    elif node.keyword in ['YEAR']:
        return __struc_breakdown_single_child(insert, node)
    
    else:
        raise NotImplementedError(f'Breakdown for {node.keyword} {node.type} is not implemented')
