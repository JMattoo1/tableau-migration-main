import unittest
from ...components import CustomTestCase

class TestTableauDaxStandardAggregation(CustomTestCase):
    """
    Class for standard conversion of aggregation from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """
    
    def _generateTests(self, keyword:str, datatype:str,twb:str, tds:str, expect:str = None):
        """
        Method to generate a list of subtest cases given a keyword
        """        

        if not expect:
            expect = keyword

        return [
            (f'{keyword.upper()}([Gender])',datatype, twb, tds, (f'{expect}( \'Buyer\'[Gender] )',0)),
            (f'{keyword.lower()}([Gender])',datatype, twb, tds, (f'{expect}( \'Buyer\'[Gender] )',0)),
            (f'{keyword}([Gender])/{keyword}([Price])',datatype, twb, tds, (f'DIVIDE( {expect}( \'Buyer\'[Gender] ), {expect}( \'Sales\'[Price] ) )',0)),
            (f'1 - {keyword.lower()}([Gender])/{keyword}([Price])',datatype, twb, tds, (f'DIVIDE( 1 - {expect}( \'Buyer\'[Gender] ), {expect}( \'Sales\'[Price] ) )',0)),
            (f'(1 - {keyword}([Gender]))/{keyword.lower()}([Price])',datatype, twb, tds, (F'DIVIDE( ( 1 - {expect}( \'Buyer\'[Gender] ) ), {expect}( \'Sales\'[Price] ) )',0)),
        ]

    def test_sum_to_sum(self):
        subTests = self._generateTests('SUM', 'real', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_avg_to_avg(self):
        subTests = self._generateTests('AVG', 'real', 'workbook1', 'sheet1','AVERAGE')

        self.runSubTests(subTests)

    def test_min_to_min(self):
        subTests = self._generateTests('MIN', 'real', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_max_to_max(self):
        subTests = self._generateTests('MAX', 'real', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_count_to_count(self):
        subTests = self._generateTests('COUNT','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

class TestTableauDaxCustomizedAggregation(CustomTestCase):
    """
    Class for customized conversion of aggregation from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_example_to_example(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass

if __name__ == '__main__':
    unittest.main()