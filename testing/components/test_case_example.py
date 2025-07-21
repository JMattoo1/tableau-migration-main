import unittest
from . import CustomTestCase # modified the relative import accordingly

class TestTableauDaxStandardExample(CustomTestCase):
    """
    Class for standard conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """
                
    def test_example_to_example(self):
        subTests = [
        ]

        self.runSubTests(subTests)

class TestTableauDaxCustomizedExample(CustomTestCase):
    """
    Class for customized conversion from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 and 1 represent Tableau and Dax function keywords
    """

    def test_example_to_example(self):
        subTests = [
        ]

        self.runSubTests(subTests)
    
if __name__ == '__main__':
    unittest.main()