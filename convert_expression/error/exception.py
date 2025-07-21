class ConversionTasksException(Exception):
    pass

class LanguageException(ConversionTasksException):
    pass

class ExpressionBreakdownException(ConversionTasksException):
    pass

class ExpressionReformException(ConversionTasksException):
    pass

class ExpressionTypeException(ConversionTasksException):
    pass

class UnforseenCaseException(ConversionTasksException):
    pass

class CorrespondingPairNotFoundException(ConversionTasksException):
    pass

class InbalancedPairFoundException(ConversionTasksException):
    pass