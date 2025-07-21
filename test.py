from unittest import TestSuite
from testing import CustomTextTestRunner, all_test_suites

if __name__ == '__main__':
    test_suite = TestSuite()

    for s in all_test_suites():
        test_suite.addTest(s)

    CustomTextTestRunner(verbosity=2).run(test_suite)