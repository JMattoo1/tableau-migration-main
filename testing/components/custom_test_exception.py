from unittest.mock import patch

class MockCustomException(Exception):
    def state(self):
        return self.__class__.state_return_value