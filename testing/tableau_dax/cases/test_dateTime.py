import unittest
from ...components import CustomTestCase

class TestTableauDaxStandardDateTime(CustomTestCase):
    """
    Class for standard conversion of datetime from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    def _generateDatepartTests(self, typeKeyword:str, datatype:str, twb:str, tds:str, expected: str=None):
        """
        Method to generate a list of subtest cases for DATEPART given an expected function
        """
        keyword = 'DATEPART'
        if not expected:
            expected = typeKeyword
        return [
            (f'{keyword.upper()}("{typeKeyword.lower()}", [date])', datatype, twb, tds, (f'{expected.upper()}( \'Sales\'[date] )',0)),
            (f'{keyword.lower()}("{typeKeyword.lower()}", [date])', datatype, twb, tds, (f'{expected.upper()}( \'Sales\'[date] )',0)),
        ]

    def _generateDatediffTests(self, typeKeyword:str, datatype:str, twb:str, tds:str):
        """
        Method to generate a list of subtest cases for DATEDIFF given an expected function
        """
        keyword = 'DATEDIFF'
        return [
            # is_required 0
            (f'{keyword.upper()}("{typeKeyword.lower()}", [date],[Parameters].[Parameter 3])', datatype, twb, tds, (f"{keyword}( 'Sales'[date], 'Parameters'[Date Parameter], {typeKeyword.upper()} )",0)),
            (f'{keyword.lower()}("{typeKeyword.lower()}", [date],[Parameters].[Parameter 3])', datatype, twb, tds, (f"{keyword}( 'Sales'[date], 'Parameters'[Date Parameter], {typeKeyword.upper()} )",0)),

            # is_required 1, TODAY not safe expression
            (f'{keyword.lower()}("{typeKeyword.lower()}", [date],today())', datatype, twb, tds, (f'{keyword}( \'Sales\'[date], TODAY(), {typeKeyword.upper()} )',1)),
            (f'{keyword.lower()}("{typeKeyword.lower()}", [date],Today())', datatype, twb, tds, (f'{keyword}( \'Sales\'[date], TODAY(), {typeKeyword.upper()} )',1)),

        ]
    # Datepart
    def test_datepart_to_second(self):
        subTests = self._generateDatepartTests('second','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_datepart_to_minute(self):
        subTests = self._generateDatepartTests('minute','integer', 'workbook1', 'sheet1')
        self.runSubTests(subTests)
        
    def test_datepart_to_hour(self):
        subTests = self._generateDatepartTests('hour','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datepart_to_day(self):
        subTests = self._generateDatepartTests('day','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datepart_to_week(self):
        subTests = self._generateDatepartTests('week', 'integer', 'workbook1', 'sheet1','weeknum')

        self.runSubTests(subTests)
    def test_datepart_to_weekday(self):
        subTests = self._generateDatepartTests('weekday','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datepart_to_month(self):
        subTests = self._generateDatepartTests('month','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datepart_to_quarter(self):
        subTests = self._generateDatepartTests('quarter','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datepart_to_year(self):
        subTests = self._generateDatepartTests('year','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    # Datediff
    def test_datediff_to_second(self):
        subTests = self._generateDatediffTests('second','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_datediff_to_minute(self):
        subTests = self._generateDatediffTests('minute','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datediff_to_hour(self):
        subTests = self._generateDatediffTests('hour','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    def test_datediff_to_day(self):
        subTests = self._generateDatediffTests('day','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datediff_to_week(self):
        subTests = self._generateDatediffTests('week','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    # def test_datediff_to_weekday(self):
    #     subTests = self._generateDatediffTests('weekday','integer','workbook1', 'sheet1')

    #     self.runSubTests(subTests)
    def test_datediff_to_month(self):
        subTests = self._generateDatediffTests('month','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datediff_to_quarter(self):
        subTests = self._generateDatediffTests('quarter','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)
    def test_datediff_to_year(self):
        subTests = self._generateDatediffTests('year','integer', 'workbook1', 'sheet1')

        self.runSubTests(subTests)

    # Dateparse
    def test_dateparse_to_format(self):
        key = 'dateparse'
        subTests = [
            (f'{key}(\'yyyy-MM-dd\', "1986-03-25")','datetime', 'workbook1','sheet1', (f'FORMAT( "1986-03-25", "yyyy-MM-dd" )',1)),
            (f'{key}(\'yyyy/MM/dd\', "1986/03/25")','datetime', 'workbook1','sheet1', (f'FORMAT( "1986/03/25", "yyyy/MM/dd" )',1)),
        ]

        self.runSubTests(subTests)

class TestTableauDaxCustomizedDateTime(CustomTestCase):
    """
    Class for customized conversion of datetime from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_DateTime_to_DateTime(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass
    
if __name__ == '__main__':
    unittest.main()