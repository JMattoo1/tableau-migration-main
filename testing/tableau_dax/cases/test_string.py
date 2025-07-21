import unittest
from ...components import CustomTestCase 

class TestTableauDaxStandardString(CustomTestCase):
    """
    Class for standard conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """
                
    def test_contains_to_containsstring(self):
        subTests = [
            (f'CONTAINS(“Calculation”, “alcu”) = true', 'boolean', 'workbook1', 'sheet1', (f'CONTAINSSTRING( “Calculation”, “alcu” ) = TRUE()',0)),
        ]

        self.runSubTests(subTests)

class TestTableauDaxCustomizedString(CustomTestCase):
    """
    Class for customized conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    # def test_String_to_String(self):
    #     subTests = [
    #     ]

    #     self.runSubTests(subTests)
    pass
    
if __name__ == '__main__':
    unittest.main()