import unittest
from ...components import CustomTestCase

class TestTableauDaxStandardTypeConv(CustomTestCase):
    """
    Class for standard conversion of type conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    def generateTests(self, keyword:str, datatype:str,twb, tds, toKeyword:str):
        return [
            (f'{keyword.upper()}(1/2)',datatype, twb, tds,(f'CONVERT( DIVIDE( 1, 2 ), {toKeyword} )',0)),
            (f'{keyword.lower()}([order])',datatype, twb, tds,(f'CONVERT( \'Sales\'[order], {toKeyword} )',0)),
            (f'{keyword}("12")',datatype, twb, tds,(f'CONVERT( "12", {toKeyword} )',0)),
        ]
                        
    def test_int_to_convert(self):
        keyword, datatype, twb, tds = "int",'integer', 'workbook1', 'sheet1'

        subTests = [
            (f'{keyword.upper()}(1/2)',datatype, twb, tds,(f'ROUNDDOWN( CONVERT( DIVIDE( 1, 2 ), DOUBLE ), 0 )',1)),
            (f'{keyword.lower()}([order])',datatype, twb, tds,(f'ROUNDDOWN( CONVERT( \'Sales\'[order], DOUBLE ), 0 )',1)),
            (f'{keyword}("12")',datatype, twb, tds,(f'ROUNDDOWN( CONVERT( "12", DOUBLE ), 0 )',1)),

        ]

        self.runSubTests(subTests)

    def test_str_to_convert(self):
        subTests = [
        ]
        subTests += self.generateTests('str', 'string', 'workbook1', 'sheet1',"STRING")

        self.runSubTests(subTests)
class TestTableauDaxCustomizedTypeConv(CustomTestCase):
    """
    Class for customized conversion of type conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_TypeConv_to_TypeConv(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass
    
if __name__ == '__main__':
    unittest.main()