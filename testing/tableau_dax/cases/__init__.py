from .test_logical import *
from .test_detailLevel import *
from .test_aggregation import *
from .test_operator import *
from .test_typeConv import *
from .test_dateTime import *
from .test_string import *
from .test_tableCal import *

# a collection of test classes
classes = [
    TestTableauDaxCustomizedLogical,
    TestTableauDaxStandardLogical,
    TestTableauDaxStandardDetailLevel,
    TestTableauDaxCustomizedDetailLevel,
    TestTableauDaxStandardAggregation,
    TestTableauDaxCustomizedAggregation,
    TestTableauDaxStandardOperator,
    TestTableauDaxCustomizedOperator,
    TestTableauDaxStandardTypeConv,
    TestTableauDaxCustomizedTypeConv,
    TestTableauDaxStandardDateTime,
    TestTableauDaxCustomizedDateTime,
    TestTableauDaxStandardString,
    TestTableauDaxCustomizedString,
    TestTableauDaxStandardTableCalculation,
    TestTableauDaxCustomizedTableCalculation
]