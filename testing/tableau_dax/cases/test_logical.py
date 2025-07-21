import unittest
from ...components import CustomTestCase, MockCustomException
# from ....convert_expression.error.exception import CorrespondingPairNotFoundException



class TestTableauDaxStandardLogical(CustomTestCase):
    """
    Class for standard conversion of logical from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 (Tableau), 1 (Dax) function keywords
    """
                
    def test_and_to_and(self):
        subTests = [
            ('[isOrder] AND [isDiscount]', 'boolean','workbook1', 'sheet1', ('[isOrder] && [isDiscount]',0)),
            ('([isOrder] AND [isDiscount]) AND ([A] AND [B])', 'boolean','workbook1', 'sheet1', ('( [isOrder] && [isDiscount] ) && ( [A] && [B] )',0)),
            ('([isOrder] AND [isDiscount]) OR ([A] AND [B])', 'boolean','workbook1', 'sheet1', ('( [isOrder] && [isDiscount] ) || ( [A] && [B] )',0)),
            ("[ZPC_TaxClassification1]='2' and [BillingDate]", 'boolean','workbook1', 'sheet1', ("[ZPC_TaxClassification1] = \"2\" && [BillingDate]",0)),
            ('[KPIBucket3]=1 AND [KPIBucket1]=1', 'boolean','workbook1', 'sheet1', ('[KPIBucket3] = 1 && [KPIBucket1] = 1',0))
        ]

        self.runSubTests(subTests)
        
    def test_or_to_or(self):
        subTests = [
            ('[isOrder] or [isDiscount]', 'boolean','workbook1', 'sheet1', ('[isOrder] || [isDiscount]',0)),
            ('([isOrder] OR [isDiscount]) AND ([A] OR [B])', 'boolean','workbook1', 'sheet1', ('( [isOrder] || [isDiscount] ) && ( [A] || [B] )',0)),
            ("[ZPC_TaxClassification1]='2' OR [BillingDate]", 'boolean','workbook1', 'sheet1', ("[ZPC_TaxClassification1] = \"2\" || [BillingDate]",0)),
            ('[KPIBucket3]=1 OR [KPIBucket1]=1', 'boolean','workbook1', 'sheet1', ('[KPIBucket3] = 1 || [KPIBucket1] = 1',0))
        ]

        self.runSubTests(subTests)

    def test_not_to_not(self):
        subTests = [
            ('NOT [isOrder] AND [isDiscount]', 'boolean','workbook1', 'sheet1', ('NOT( [isOrder] ) && [isDiscount]',0)),
            ('([isOrder] OR not [isDiscount]) AND NOT ([A] OR [B])', 'boolean','workbook1', 'sheet1', ('( [isOrder] || NOT( [isDiscount] ) ) && NOT( ( [A] || [B] ) )',0)),
        ]

        self.runSubTests(subTests)

    def test_isnull_to_isblank(self):
        subTests = [
            ('isnull([A])', 'boolean','workbook1', 'sheet1', ('ISBLANK( [A] )', 0)),
            ('ISNULL([A])', 'boolean','workbook1', 'sheet1', ('ISBLANK( [A] )', 0)),
            (f'isNull([Sales]+[SalesItem])', 'boolean','workbook1', 'sheet1', (f'ISBLANK( \'Sales\'[Sales] + \'Sales\'[SalesItem] )',0)),
            (f'ISNULL([date])', 'boolean','workbook1', 'sheet1', (f'ISBLANK( \'Sales\'[date] )',0)),
        ]

        self.runSubTests(subTests)

class TestTableauDaxCustomizedLogical(CustomTestCase):
    """
    Class for customized conversion of logical from Tableau to Dax
    Method is named from test_{0}_to_{1}, where 0 (Tableau), 1 (Dax) function keywords
    """

    def test_if_to_switch(self):
        subTests = [
            # is_required = 0
            ("if [order] then 0 else 1 end",'integer','workbook1', 'sheet1', ('SWITCH( TRUE(), \'Sales\'[order], 0, 1 )',0)),
            ("IF [KPIBucket1]=1 THEN 'Hit' ELSE 'Missed' END",'string', 'workbook1', 'sheet1', ("SWITCH( TRUE(), [KPIBucket1]"\
                " = 1, \"Hit\", \"Missed\" )", 0)),

            ("IF (CASE [KPIBucket1] WHEN 1 THEN 'Hit' ELSE 'Missed' END)='Hit' THEN 1 "\
                "ELSEIF (CASE [KPIBucket1] WHEN 1 THEN 'Hit' ELSE 'Missed' END)='Missed' THEN 2 END", 'string', 'workbook1', 'sheet1',
                ("SWITCH( TRUE(), ( SWITCH( TRUE(), [KPIBucket1] = 1, \"Hit\", \"Missed\" ) ) = \"Hit\""\
                 ", 1, ( SWITCH( TRUE(), [KPIBucket1] = 1, \"Hit\", \"Missed\" ) ) = \"Missed\", 2 )", 0)),
            
            ("if [order]>5000000 \nthen '超過500萬' \nelse \nif [order]>3000000\n"\
                "then '超過300萬'\nelse \nif [order]>1000000\nthen '超過100萬'\nelse \n"\
                "if [order]>500000\nthen '超過50萬'\nelse ''\nEND\n\nEND\n\nEND\n\nEND", 
                "string", 'workbook1', 'sheet1',('SWITCH( TRUE(), \'Sales\'[order] > 5000000, "超過500萬", SWITCH( TRUE(), ' \
                '\'Sales\'[order] > 3000000, "超過300萬", SWITCH( TRUE(), \'Sales\'[order] > 1000000,'\
                ' "超過100萬", SWITCH( TRUE(), \'Sales\'[order] > 500000, "超過50萬", "" ) ) ) )',0)),
            
            ('if [ShippedDate] = Null  then "NULL" else "NOT NULL"'\
                'END', "string", 'workbook1', 'sheet1', (f'SWITCH( TRUE(), ISBLANK( \'Orders\'[Shipped Date] ),'\
                ' "NULL", "NOT NULL" )',0)),

            ('IF  [Name]="name1" then "n1" ELSEIF  [Name]="name2" then '\
                '( if [postal]="100000" then "n1" ELSEIF [postal]="100001'\
                '" then "n1" END) ELSE (if [ShipRegion]="r1" then "n1" '\
                'ELSEIF [ShipRegion]="r12" then "n2" ELSEIF [ShipRegion]='\
                '"A" and [ShipRegion]="-"  then ( if [postal]="100001" then'\
                ' "n1" elseif [postal]="100002" then "n2" else "n3" End '\
                ') ELSEIF [ShippersName]="" and [SupplierContanct]="" then '\
                '( if [postal]="100001" then "n1" elseif [postal]="100002"'\
                ' then "n2" Else "" END ) else "" END ) END', 
            'string', 'workbook1', 'sheet1', 
            (f'SWITCH( TRUE(), \'Buyer\'[Name] = "name1", "n1", \'Buyer\'['\
                'Name] = "name2", ( SWITCH( TRUE(), \'Orders\'[Ship Postal '\
                'Code] = "100000", "n1", \'Orders\'[Ship Postal Code] = '\
                '"100001", "n1" ) ), ( SWITCH( TRUE(), \'Orders\'[Ship Region]'\
                ' = "r1", "n1", \'Orders\'[Ship Region] = "r12", "n2",'\
                ' \'Orders\'[Ship Region] = "A" && \'Orders\'[Ship Region]'\
                ' = "-", ( SWITCH( TRUE(), \'Orders\'[Ship Postal Code] ='\
                ' "100001", "n1", \'Orders\'[Ship Postal Code] = "100002", '\
                '"n2", "n3" ) ), \'Orders\'[Shippers Name] = "" && \'Produ'\
                'cts\'[Supplier Contanct] = "", ( SWITCH( TRUE(), \'Orders\'['\
                'Ship Postal Code] = "100001", "n1", \'Orders\'[Ship Postal '\
                'Code] = "100002", "n2", "" ) ), "" ) ) )',0)),
            

        ]

        errors = [
            # is_required = 1
            ("if [order] then 0 else 1", 'integer','workbook1', 'sheet1', ('IF \'Sales\'[order] THEN 0 ELSE 1',1)),
            ("if [order]<80 then 0 ELSEIF [order]<50 THEN 1 ELSE 3",'integer','workbook1', 'sheet1', ('IF \'Sales\'[order] < 80'\
                ' THEN 0 ELSEIF \'Sales\'[order] < 50 THEN 1 ELSE 3',1)),
        ]

        self.runSubTests(subTests)

        for x in errors:
            print(f'{x[0]};{x[1]}')
            with self.subTest(x=x):
                MockCustomException.state_return_value = True
                self.assertEqual(self._instance.convert(x[0], x[1], x[2], x[3]), x[-1])

    def test_ifnull_to_if(self):
        subTests = [
            (f'IFNULL([Name]," ")','string', 'workbook1', 'sheet1', (f'IF( NOT( ISBLANK( \'Buyer\'[Name] ) ), \'Buyer\'[Name], " " )',0)),
            (f'ifnull(str(int([Measure1])),[Measure1])','real', 'workbook1', 'sheet1', (f'IF( NOT( ISBLANK( CONVERT( ROUNDDOWN( CONVERT( \'Measure Tables\'[Measure1], DOUBLE ), 0 ), STRING ) ) ), CONVERT( ROUNDDOWN( CONVERT( \'Measure Tables\'[Measure1], DOUBLE ), 0 ), STRING ), \'Measure Tables\'[Measure1] )',1)),
        ]

        self.runSubTests(subTests)

    def test_zn_to_if(self):
        subTests = [
            (f'ZN([order])','real', 'workbook1', 'sheet1', (f'IF( ISBLANK( \'Sales\'[order] ), 0, \'Sales\'[order] )',0)),
            (f'ZN([Measure1])-[Measure2]','real', 'workbook1', 'sheet1', (f'IF( ISBLANK( \'Measure Tables\'[Measure1] ), 0, \'Measure Tables\'[Measure1] ) - \'Measure Tables\'[Measure2]',0)),
        ]
        
        self.runSubTests(subTests)

if __name__ == '__main__':
    unittest.main()