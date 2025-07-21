from config import *
import os
import pandas as pd
from convert_expression.languages.tableau import _type
from itertools import chain
import re

if __name__ == '__main__':
    file = outFilePath + inFolderName + '.xlsx'
    column = pd.read_excel('Batch_1_Analysis_Combined (4).xlsx', index_col=0, sheet_name='column')

    keys = list(chain.from_iterable([_type.get(x) for x in _type.keys()]))
    types = dict.fromkeys(keys, 0)

    for _, row in column.iterrows():
        formula = str(row['formula'])
        for k in keys:
            count = formula.split().count(k)
            if count:
                types[k] += count

    df = pd.DataFrame(types.items())
    df.to_csv('dump/analyze.csv', encoding='utf-8')
