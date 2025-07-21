import unittest
from ...components import CustomTestCase

class TestTableauDaxStandardDetailLevel(CustomTestCase):
    """
    Class for standard conversion of detail level from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """
                
    def test_fixed_to_calculate(self):
        subTests = [
            ('{Fixed : SUM([A])}', 'real','workbook1', 'sheet1', ('CALCULATE( SUM( [A] ) )', 0)),
            ('{Fixed [order]: SUM([A])}','real','workbook1', 'sheet1',  ('CALCULATE( SUM( [A] ), ALLEXCEPT( \'Sales\', \'Sales'\
                '\'[order] ) )', 0)),
            ('{Fixed [order], [Price]: SUM([A])}', 'real','workbook1', 'sheet1',  ('CALCULATE( SUM( [A] ), ALLEXCEPT( \'Sales\','\
                ' \'Sales\'[order] ), ALLEXCEPT( \'Sales\', \'Sales\'[Price] ) )', 0)),
        ]

        self.runSubTests(subTests)

class TestTableauDaxCustomizedDetailLevel(CustomTestCase):
    """
    Class for customized conversion of detail level from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_example_to_example(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass

if __name__ == '__main__':
    unittest.main()