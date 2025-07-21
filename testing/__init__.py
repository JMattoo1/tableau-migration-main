from .tableau_dax import loader as td_loader
from .components import CustomTextTestRunner

def all_test_suites():
    suites = []
    
    suites+=td_loader()

    return suites