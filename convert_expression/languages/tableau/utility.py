from ...utility import find_patterns_used, find_corresponding_closing_index
from ...error import CorrespondingPairNotFoundException

def find_pattern_indices(patterns:list,data:list, size:int) -> tuple[list, bool]:
    """
    find positions for patterns, and if it is a balanced set
    """
    indices=[]
    for index, ele in enumerate(data):
        if ele in patterns:
            indices.append(index)

    return indices, len(indices)%size == 0

def remove_nested_position_of_functions_with_same_closing(positions:list, pair:dict,ending:str, data:list = None):
    """
    Remove number in positions for nested function with same closing
    """
    func = pair[ending]
    
    if len(ending) <= 1:
        raise ValueError(f'Expected functions but given {func}. This function does not share same ending {ending} with other functions')

    tempPos = []
    stack = []
    nestedPosition:dict[int, list] = {}
    key = 0

    for i, v in enumerate(positions):
        if data[v] in func or data[v] == ending:
            tempPos.append(i)
    
    for i, v in enumerate(tempPos):
        if data[positions[v]] in func:
            # func
            if not stack:
                stack.append(v)
            else:
                nestedPosition[len(nestedPosition)] = [v]
                key = len(nestedPosition) - 1
        else:
            # ending
            if key in nestedPosition.keys() and len(nestedPosition[key]) == 1:
                nestedPosition[key].append(v)
                key-=1
            else:
                isLast = True
                for x in range(key-1,-1,-1):
                    if len(nestedPosition[x]) == 1:
                        nestedPosition[x].append(v)
                        key = x - 1
                        isLast = False
                        break
                if isLast:
                    stack.pop()

    newPos = positions.copy()

    for x in reversed(nestedPosition):
        start = nestedPosition[x][0]
        end = nestedPosition[x][1]
        
        for x in range(start, end+1):
            newPos[x] = None

    return list(filter(None.__ne__,newPos))

def get_outer_most_position_of_functions(positions:list,result:list = None, data:list = None, startPos:int = None):
    """
    Return positions of outer most functions 
    """
    for i, v in enumerate(positions):
        if i >= startPos:
            match data[v]:
                case 'IF' | 'CASE':
                    # special handling for 'IF' and 'CASE'
                    patterns = ["IF","ELSEIF", "ELSE","THEN", "END" , "CASE","WHEN"]
                    patterns = find_patterns_used(patterns, data)
                    opening = data[v]
                    closing = 'END'

                case 'END' | ')' | '}':
                    # ignore these keywords
                    continue

                case '{':
                    # special handling for curly open bracket
                    patterns = ['{','}']
                    opening = "{"
                    closing = "}"

                case _:
                    # handle other keywords
                    special = [
                        # detail level
                        'FIXED',
                        # operators
                        "+", "-", "*", "/", "%", 
                        "==", "=", ">", "<", ">=", 
                        "<=", "!=", "<>", "^"
                    ]
                    groups = ['(',')', '{','}']
                    if data[v] in special or data[v] not in groups:
                        # special handling for operators, fixed
                        result.append(v)
                        continue

                    patterns = ["(", ")"]
                    opening = "("
                    closing = ")"

            result.append(v)
            tempPositions = [index for index,_ in enumerate(data) if data[index] in patterns]
            if opening == '(':
                openPos = data[:positions[i]+1].count('(') - 1
            else:
                openPos = 0

            if data[v] in ['CASE', 'IF']:
                tempPositions = remove_nested_position_of_functions_with_same_closing(tempPositions, {closing:['CASE', 'IF']},closing,data)
            
            closePos = find_corresponding_closing_index(tempPositions,opening, closing, data, openPos, {closing:opening})
            if closePos is None:
                # Unable to find ending of the statement
                # raise OpenClosePairException(f'Cannot find corresponding {opening}-{closing} pair')
                # print(f'close pair not found {[data[ele] for ele in tempPositions]}')
                raise CorrespondingPairNotFoundException(f'Cannot find corresponding {opening}-{closing} pair for {data} {openPos} {i}:{v} {tempPositions} {data[:positions[i]+1]} {data[:positions[i]+1].count("(") - 1}')

            result.append(tempPositions[closePos])
            
            if positions.index(tempPositions[closePos]) == (len(positions) - 1):
                # found last outest most element
                return result
            else:
                # continue to find outest most elements
                startPos = positions.index(tempPositions[closePos]) + 1

    return result