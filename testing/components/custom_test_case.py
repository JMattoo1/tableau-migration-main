import unittest
from convert_expression.instance import createInstances
from .custom_test_exception import *

class CustomTestCase(unittest.TestCase):
    """
    Class customized test case derived from unittest's TestClass
    """

    # Sample label references
    colRef = {
        'workbook1': {
            'sheet1': {
                '[Gender]': "'Buyer'[Gender]", 
                '[Name]': "'Buyer'[Name]", 
                '[Price]': "'Sales'[Price]",
                '[order]': "'Sales'[order]",
                '[Sales]': "'Sales'[Sales]",
                '[SalesItem]': "'Sales'[SalesItem]",
                '[date]': "'Sales'[date]",
                '[top5]': '[TOP 5 Rank Filter]', 
                '[postal]': "'Orders'[Ship Postal Code]", 
                '[ShipRegion]': "'Orders'[Ship Region]", 
                '[ShippedDate]': "'Orders'[Shipped Date]", 
                '[ShippersName]': "'Orders'[Shippers Name]", 
                '[SupplierContanct]': "'Products'[Supplier Contanct]", 
                '[SupplierID]': "'Products'[Supplier ID]", 
                '[Parameters].[Parameter 2]': "'Parameters'[Metric Parameter]",
                '[Parameters].[Parameter 1]': "'Parameters'[Include Parameter]",
                '[Parameters].[Parameter 3]': "'Parameters'[Date Parameter]",
                '[Parameters].[Calculation_2345 (copy)]': "'Parameters'[Real]",
                '[Measure1]': "'Measure Tables'[Measure1]",
                '[Measure2]': "'Measure Tables'[Measure2]",
            }
        }

    }

    def setUp(self) -> None:
        self._instance = createInstances(None)
        self._instance.colRef = self.colRef
        custom_exception_patcher = patch(
            'convert_expression.error.exception.CorrespondingPairNotFoundException',
            new=MockCustomException
        )
        # start patcher
        custom_exception_patcher.start()
        self.addCleanup(custom_exception_patcher.stop)

        return super().setUp()
    
    def tearDown(self) -> None:
        del self._instance
        return super().tearDown()

    def runSubTests(self, subTests):
        """
        Run a list of subtests
        """
        print()
        for x in subTests:
            print(f'{";".join(x[:-1])};{x[-1]}')
            with self.subTest(x=x):
                self.assertEqual(self._instance.convert(x[0],x[1], x[2], x[3]), x[-1])
