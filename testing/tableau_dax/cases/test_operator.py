import unittest
from ...components import CustomTestCase

class TestTableauDaxStandardOperator(CustomTestCase):
    """
    Class for standard conversion of operator from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    def _generateArithmeticTests(self, keyword:str, datatype:str, twb:str, tds:str,expect:str = None):
        """
        Method to generate a list of subtest cases for Arithmetic Operators given the operator and an expected function
        """
        if not expect:
            expect = keyword 
            
        return [
            (f'1{keyword}[c]', datatype, twb, tds, (f'1 {expect} [c]',0)),
            (f'-1{keyword}[c]', datatype, twb, tds, (f'-1 {expect} [c]',0)),
            (f'(1{keyword}[c]){keyword}10', datatype, twb, tds, (f'( 1 {expect} [c] ) {expect} 10',0)),
            (f'(1{keyword}[c])/10', datatype, twb, tds, (f'DIVIDE( ( 1 {expect} [c] ), 10 )',0)),
            (f'(1{keyword}[c])*10', datatype, twb, tds, (f'( 1 {expect} [c] ) * 10',0)),
            (f'(1{keyword}[Parameters].[Calculation_2345 (copy)])*10', datatype, twb, tds, (f'( 1 {expect} \'Parameters\'[Real] ) * 10',0)),
        ]
    def _generateComparisonTests(self, keyword:str, datatype:str, twb:str, tds:str,expect:str = None):
        """
        Method to generate a list of subtest cases for Comparison Operators given the operator and an expected function
        """
        if not expect:
            expect = keyword 
            
        return [
            (f'1{keyword}[c]', datatype, twb, tds, (f'1 {expect} [c]',0)),
            (f'-1{keyword}[c]', datatype, twb, tds, (f'-1 {expect} [c]',0)),
            (f'(1{keyword}[c]){keyword}10', datatype, twb, tds, (f'( 1 {expect} [c] ) {expect} 10',0)),
        ]

    def _customGenerateTests(self, keyword:str, datatype:str, twb:str, tds:str, expect:str = None):
        """
        Method to generate a list of subtest cases for Operators given the operator and an expected function
        """
        if not expect:
            expect = keyword 
            
        return [
            (f'1{keyword}[c]', datatype, twb, tds, (f'{expect}( 1, [c] )',0)),
            (f'(1{keyword}[c]){keyword}10', datatype, twb, tds, (f'{expect}( ( {expect}( 1, [c] ) ), 10 )',0)),
            (f'(1{keyword}[c])/10', datatype, twb, tds, (f'DIVIDE( ( {expect}( 1, [c] ) ), 10 )',0)),
            (f'(1{keyword}[c])*10', datatype, twb, tds, (f'( {expect}( 1, [c] ) ) * 10',0)),
        ]

    def test_addition_to_addition(self):
        subTests = self._generateArithmeticTests('+','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_divide_to_divide(self):
        subTests = [
            (f'1/[c]', 'real', 'workbook1', 'sheet1',(f'DIVIDE( 1, [c] )',0)),
            (f'-1/[c]', 'real', 'workbook1', 'sheet1',(f'DIVIDE( -1, [c] )',0)),
            (f'(1/[c])/10', 'real', 'workbook1', 'sheet1',(f'DIVIDE( ( DIVIDE( 1, [c] ) ), 10 )',0)),
            (f'(1/[c])/10', 'real', 'workbook1', 'sheet1',(f'DIVIDE( ( DIVIDE( 1, [c] ) ), 10 )',0)),
            (f'(1/[c])*10', 'real', 'workbook1', 'sheet1',(f'( DIVIDE( 1, [c] ) ) * 10',0)),
            (f'IF [ShippedDate]<#09/13/21# THEN [Measure1] ELSEIF [ShippedDate]>=#09/13/21# THEN [Measure2] '\
             'END', 'real', 'workbook1', 'sheet1', (f'SWITCH( TRUE(), \'Orders\'[Shipped Date] < DATE( 2021, 9, '\
                '13 ), \'Measure Tables\'[Measure1], \'Orders\'[Shipped Date] >= DATE( 2021, 9, 13 ), \'Measure Tables\'[Measure2] )', 0)),
            (f'IF [ShippedDate]<#09/13/2021# THEN [Measure1] ELSEIF [ShippedDate]>=#09/13/2021# THEN [Measure2] '\
             'END', 'real', 'workbook1', 'sheet1', (f'SWITCH( TRUE(), \'Orders\'[Shipped Date] < DATE( 2021, 9, '\
                '13 ), \'Measure Tables\'[Measure1], \'Orders\'[Shipped Date] >= DATE( 2021, 9, 13 ), \'Measure Tables\'[Measure2] )', 0))
        ]

        self.runSubTests(subTests)

    def test_minus_to_minus(self):
        subTests = self._generateArithmeticTests('-','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_multiply_to_multiply(self):
        subTests = self._generateArithmeticTests('*','real', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    
    def test_divisor_to_divisor(self):
        subTests = self._customGenerateTests('%','integer','workbook1', 'sheet1','MOD')

        self.runSubTests(subTests)

    def test_eq_to_eq(self):
        subTests = self._generateComparisonTests('=','boolean', 'workbook1', 'sheet1')
        subTests += self._generateComparisonTests('==','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_lt_to_lt(self):
        subTests = self._generateComparisonTests('<','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_gt_to_gt(self):
        subTests = self._generateComparisonTests('>','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_lte_to_lte(self):
        subTests = self._generateComparisonTests('<=','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_gte_to_gte(self):
        subTests = self._generateComparisonTests('>=','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_ne_to_ne(self):
        subTests = self._generateComparisonTests('!=', 'boolean', 'workbook1', 'sheet1','<>')
        subTests += self._generateComparisonTests('<>','boolean', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_expo_to_expo(self):
        subTests = self._generateArithmeticTests('*','real', 'workbook1', 'sheet1')

        self.runSubTests(subTests)



class TestTableauDaxCustomizedOperator(CustomTestCase):
    """
    Class for customized conversion of operator from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_division_to_division(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass
if __name__ == '__main__':
    unittest.main()