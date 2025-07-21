import unittest
from ...components import CustomTestCase 

class TestTableauDaxStandardTableCalculation(CustomTestCase):
    """
    Class for standard conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_TableCalculation_to_TableCalculation(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass

class TestTableauDaxCustomizedTableCalculation(CustomTestCase):
    """
    Class for customized conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    def test_total_to_calculate(self):
        keyword = 'tOtal'
        subTests = [
            # is_required 0
            (f'{keyword}(SUM([order]))','real', 'workbook1', 'sheet1', (f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
            (f'{keyword.upper()}(SUM([order]))','real', 'workbook1', 'sheet1', (f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
            (f'{keyword.lower()}(sum([order]))','real', 'workbook1', 'sheet1', (f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
            # ('TOTAL ( SUM ( IF [NoSalesin3Months] = "No" THEN 1 ELSE 0 END ) )', 'real', ('',0)),
            # ('TOTAL ( SUM ( [Loose Pick Quantity] ) / SUM ( { FIXED [Plant] , [PrincipalName] , [isTrialLens] , '\
            #  '[ProductClass] : SUM ( [Loose Pick Quantity] ) } ) )','real', 'workbook1', 'sheet1', ('',0))
        ]

        self.runSubTests(subTests)
    
    # INDEX requires context injection (recongizes the table and column it applies to)
    # def test_index_rankx(self):
    #     keyword = 'Index'
    #     subTests = [
    #         # is_required 0
    #         (f'{keyword}()',(f'RANKX(  )',0)),
    #         (f'{keyword.upper()}()',(f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
    #         (f'{keyword.lower()}()',(f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
    #         (f'{keyword.upper()}()<=[Parameters].[Parameter 2]',(f'CALCULATE( SUM( \'Sales\'[order] ), ALL( \'Sales\' ) )',0)),
    #     ]

    #     self.runSubTests(subTests)
    
if __name__ == '__main__':
    unittest.main()