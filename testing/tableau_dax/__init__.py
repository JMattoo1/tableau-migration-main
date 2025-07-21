from .cases import classes
from unittest import TestLoader

def loader():
    """
    Return a list of suites given a collectio of classes
    """
    test_loader = TestLoader()
    suites = []
    for c in classes:
        suite = test_loader.loadTestsFromTestCase(c)
        suites.append(suite)

    return suites