from config import custom, fromLanguage, toLanguage
from .expression import Tree, Node
import pandas as pd 
from .languages import get_from_to_languages, get_translator
from .utility import *
import re
from .error import *
import traceback
import os
from tqdm import tqdm
from .constant import logger

def createInstances(colRef:pd.DataFrame):
    return Convert_Expression(colRef)

class Convert_Expression:
    """
    Class Convert_Expression
    """
    sub = {}
    
    def __init__(self, colRef:pd.DataFrame) -> None:
        self.colRef = self.__get_col_ref_value(colRef)
        # df = pd.DataFrame(self.colRef.items())
        # with pd.ExcelWriter('colref.xlsx') as writer:
        #     # test.to_excel(writer, sheet_name='Sheet1', index=False)
        #     df.to_excel(writer, sheet_name='column', index=False)
        
        self.fromLanguage, self.toLanguage  = get_from_to_languages(fromLanguage, toLanguage)
        fromType, fromTypePrecedence = self.fromLanguage.variables
        fromEvaluate, fromGetType, fromGetTypeOnNext = self.fromLanguage.utilities

        self.registry, implExpression, safeExpression = get_translator(custom, fromLanguage, toLanguage)

        self.implExpression, self.safeExpression = implExpression, safeExpression if fromLanguage != toLanguage else self.toLanguage.expressions

        toInterpreter = self.toLanguage.interpreter
        fromInterpreter = self.fromLanguage.interpreter
        self.tree = Tree(
            typePrecedence=fromTypePrecedence,
            type= fromType, 
            registry= self.registry,
            evaluate= fromEvaluate,
            get_type= fromGetType,
            get_type_on_next_keyword= fromGetTypeOnNext,
            fromInterpreter= fromInterpreter,
            toInterpreter= toInterpreter, 
            isTranslate= fromLanguage != toLanguage,
            safeExpressionList=self.safeExpression
        )

    def __get_col_ref_value(self, colRef:pd.DataFrame):
        """
        Convert column in Tableau's syntax to match Dax's syntax <Tablea's column>: <DAX's TableColumn | Measure | Parameters>
        """
        if colRef is None or colRef.empty:
            return {}
        
        result:dict[str,dict[str, dict[str, str]]] = {}
        col_ref_log = tqdm(total=len(colRef.index), desc='column reference')

        for _, row in colRef.iterrows():
            type = row["column_type"]
            key = f'[{row["column_id"]}]' if type !="PARAMETER" else f"[Parameters].{row['column_id']}"
            value = row['tableau_field_name']
            twb = row['twb']
            tds = row['tds']

            if twb not in result.keys():
                result[twb] = {tds: {}}
            elif tds not in result[twb].keys():
                result[twb][tds] = {key: ""}

            if type == "BASE":
                table = re.split('[\s()]',row['tableRefName'] if not "nan" else "")[0]
                value = remove_extra_space(re.sub(r"([\(\[].*?[\)\]])","",value))
                result[twb][tds][key] = f"'{table}'[{' '.join(value)}]" if table else f"[{' '.join(value)}]"

            elif type == "DERIVED":
                value = remove_extra_space(value)
                result[twb][tds][key] = f"[{' '.join(value)}]"

            elif type == "PARAMETER":
                # Assuming there is a table named "Parameters" that store value of parameters
                result[twb][tds][key] = f"'Parameters'[{value}]"

            else:
                col_ref_log.close()
                raise ValueError(f"Expected value 'BASE','PARAMETER' and 'DERIVED', but given {row['column_type']}")
            
            col_ref_log.update(1)
        return result
        

    def __label(self, string:str, twb:str, tds:str) -> tuple[str, list, dict]:
        """
        label all found column reference        
        """
        foundKey = []
        sub = {}
        patterns = self.colRef[twb][tds].keys()
        occurColRef = self.__find_col_ref(string)
        occurstring = self.__find_String_Lit(string)
        newString = string

        if any(p in string for p in patterns):
            # replace every matched col ref with [<id>]
            for key in patterns:
                if key in string:
                    newString = newString.replace(key, f" [{len(sub)}] ")
                    sub[len(sub)] = key
                    foundKey.append(key)
        for o in occurColRef:
            if o not in foundKey:
                newString = newString.replace(o, f" [{len(sub)}] ")
                foundKey.append(o)
                sub[len(sub)] = o
        for o in occurstring:
            newString = newString.replace(o, f" [{len(sub)}] ")
            if o.startswith("'") and o.endswith("'"):
                o = f'"{o[1:-1]}"'
            foundKey.append(o)
            sub[len(sub)] = o
        string = newString

        df = pd.DataFrame(sub.items())
        df['tds'] = pd.Series([tds for x in range(len(df.index))], dtype='object')
        df['twb'] = pd.Series([twb for x in range(len(df.index))], dtype='object')
        if os.path.exists('colref2.csv'):
            df.to_csv('colref2.csv', encoding='utf-8', mode='a', header=False)
        else:
            df.to_csv('colref2.csv', encoding='utf-8', header=False)

        return string, foundKey, sub
    
    def __find_col_ref(self, string):
        pattern = r'(\[Parameters\]\.\[[0-9A-Za-z\s\(\)_]+\])|(\[.*?\])'
        regex = re.compile(pattern)
        return [x if x else y for x,y in regex.findall(string)]

    def __find_String_Lit(self, string) -> list[str]:
        pattern = r'(\'.*?\')|(\".*?\")'
        regex = re.compile(pattern)

        return [x if x else y for x,y in regex.findall(string)]

    # def remove_inline_comments(string: str):
    #     """
    #     Remove inline comments in the epxression
    #     """
    #     pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    #     regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    #     def _replacer(match):
    #         # if the 2nd group (capturing comments) is not None,
    #         # it means we have captured a non-quoted (real) comment string.
    #         if match.group(2) is not None:
    #             return "" # so we will return empty to remove the comment
    #         else: # otherwise, we will return the 1st group
    #             return match.group(1) # captured quoted-string
    #     return regex.sub(_replacer, string)

    def __sub_col_ref(self, string:str,twb:str, tds:str) -> str:
        """
        substitute all labels with found column reference
        """
        for key in self.sub.keys():
            replaceWith:str = self.colRef[twb][tds][self.sub[key]] if self.sub[key] in self.colRef[twb][tds].keys() else self.sub[key]
            string = re.sub(rf"(\[{key}\])", replaceWith.replace('\\', '\\\\'), string)
        return string

    def convert(self, string:str, datatype:str, twb:str, tds:str):
        """
        convert to dax with Tablea expressions storing in tree structure
        """
        try:
            logger.info('convert start')

            if not string:
                return "", 0

            newString = str(string)

            # Step 1: Identify and Substitute Col Ref and String Literal Expression
            newString, foundKey, self.sub = self.__label(newString, twb, tds)

            # Step 2: Clean expression, focus on adding spaces between all operators and brackets
            newString = remove_inline_comments(newString)
            newString = add_spaces_to_sides(newString, [r'[{\}:]',r'(#[0-9/]+#|>=|<=|<>|==|!=|=|%|<|>|/|\+|,|\*|-)'])

            # Step 3: Clean expression by adding spaces between parenthesis and end of line sperators
            newString = add_spaces_to_sides(newString, [r'[()\r\n]'])
            newString = remove_newline(newString)

            # Step 3: Identify and Separate Expression from Fixed LOD
            newString = remove_extra_space(newString)
            string = newString
            
            # print(f'inserting {original}')
            # Step 4: Identify and Further breakdown all nested nodes by functions
            root = None
            root = self.tree.insert(root,newString, string)
            # self.tree.traversePreorder(root)

            # Step 5: Identify Dax Equivalent Formula and Convert to Dax by recurively combine expressions from children at all level
            data, req_reviews = self.__get_expression(root,self.__sub_col_ref,datatype, twb, tds)

            # # Step 6: Sub back Col Ref <- substitution happens during expression as some expressions require table name 
            data = self.__sub_col_ref(data, twb, tds)
            
            return data, req_reviews
        except Exception as err:
            if issubclass(err.__class__,ConversionTasksException):
                # if isinstance(err, ExpressionBreakdownException):
                # traceback.print_exc()
                pass
            elif isinstance(err, NotImplementedError):
                pass
            else:
                traceback.print_exc()
            logger.warning(err, exc_info=True)
            # print(re.sub(r'[\r\n]', "", " ".join(string)))
            string = self.__sub_col_ref(" ".join(string), twb, tds)
            # print(string)
            return string, 1
        finally:
            logger.info('convert end')

    
    def __get_expression(self, node:Node, sub_col_ref, datatype:str, twb:str, tds: str):
        """
        Return an equivalent expression and if required review
        """
        if node is not None:
            self.tree.traverse_shift_nodes(node)
        return self.tree.traverseForExpression(node, sub_col_ref, datatype, twb, tds)
