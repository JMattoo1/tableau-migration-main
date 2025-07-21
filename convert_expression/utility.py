import re
from .expression import Node

# Utility function
def remove_extra_space(string:str):
    """
    remove extra spaces while retaining the spaces between words
    """
    return list(filter("".__ne__,string.split(" ")))

def add_spaces_to_sides(string: str, regrex: str|list):
    """
    add spaces to sides of pattern(s)
    """
    if isinstance(regrex,str):
        return  re.sub(regrex, ' \g<0> ', string)
    elif isinstance(regrex,list):
        return re.sub(re.compile("|".join(regrex)), ' \g<0> ', string)
    else:
        raise TypeError(f'Expected type of list of str but given {type(regrex)}')

def remove_extra_space(string:str):
    """
    remove extra spaces while retaining the spaces between words
    """
    return list(filter("".__ne__,string.split(" ")))

def remove_newline(string:str):
    return re.sub(r'[\r\n]', " ", string)

def find_patterns_used(patterns:list, data:list)-> list:
    """
    find the used patterns based on a set of patterns 
    """
    return list(p for p in patterns if p in data or p in data)

def remove_nested_position_of_same_function(opening:str, closing:str, data:list[str], positions:list):
    """
    Remove number in positions for nested of same function
    """
    if all([opening, closing, data, positions]):

        nestedPosition:dict[int, list] = {}
        newPosition = []
        
        stack = []
        for i, v in enumerate(positions) :
            if i > 0 and i < len(positions) -1:
                if data[v] == opening :
                    stack.append(opening)
                    nestedPosition[len(nestedPosition)] = [i]
                elif data[v] == closing :
                    if not stack:
                        # raise ValueError(f"Given data {data} does not have a proper {opening}-{closing} statement, {positions}")
                        raise ValueError(f"Does not have a proper {opening}-{closing} statement")
                    else:
                        stack.pop()
                        if stack:
                            # insert from the back
                            for x in range(len(nestedPosition)-1, -1):
                                if len(nestedPosition[x]) == 1:
                                    nestedPosition[len(nestedPosition)-1].append(i)
                        else:
                            # insert from the front
                            for x in range(0, len(nestedPosition)):
                                if len(nestedPosition[x]) == 1:
                                    nestedPosition[len(nestedPosition)-1].append(i)
                else:
                    continue
            else:
                continue
        newPosition = positions.copy()
        for x in reversed(nestedPosition):

            start = nestedPosition[x][0]
            end = nestedPosition[x][1]
            if end == len(newPosition) - 1:
                newPosition = newPosition[0:start]
            else:
                newPosition = newPosition[0:start] + newPosition[end + 1:]
        return newPosition
    return None

def find_corresponding_closing_index(positions:list, opening:str, closing:str,data:list[str], openPos, pair):
    """
    get the corresponding index of closing in data
    """
    stack = []
    for i, v in enumerate(positions) :
        if data[v] == opening :
            stack.append(opening)
        elif data[v] == closing :
            if not stack:
                return None
            else:
                pop = stack.pop()
                if pop != pair[closing]:
                    # opening or closing does not match
                    return None
                else:
                    # found a closing
                    if stack:
                        # not correct closing
                        continue
                    elif len(stack) == openPos:
                        # correct closing
                        return i
                    else:
                        return len(positions) - 1
        else:
            continue

    return None

def remove_inline_comments(string: str):
    """
    Remove inline comments in the epxression
    """
    # pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    # def _replacer(match):
    #     # if the 2nd group (capturing comments) is not None,
    #     # it means we have captured a non-quoted (real) comment string.
    #     if match.group(2) is not None:
    #         return "" # so we will return empty to remove the comment
    #     else: # otherwise, we will return the 1st group
    #         return match.group(1) # captured quoted-string
    # return regex.sub(_replacer, string)
    return re.sub(r'//.*','', string)