# Unit Testing
import pandas as pd
import numpy as np
from convert_expression import instance as ce
from tqdm import tqdm
import glob
import os

column_ignore_column_id = [
    # formulat truncated


]

column_only_column_id = [

]

outFilename = 'dump/test_custom.xlsx'
path = "C:/Users/zhi4949/projects/Test tool/"
inFileNames = glob.glob(path + "\*.xlsx")

result = dict()


if __name__ == '__main__':
    outer = tqdm(total=len(inFileNames), desc='Files', position=0)
    file_log = tqdm(total=0, bar_format='{desc}', position=1)
    sheet_log = tqdm(total=0, bar_format='{desc}', position=2)

    for f in inFileNames:
        xls = pd.ExcelFile(f)
        sheets = xls.sheet_names
        inner = tqdm(total=len(sheets), desc='Sheets', position=3)
        file_log.set_description_str(f'Current file: {f}')
        for s in xls.sheet_names:
            sheet_log.set_description_str(f'Current sheet: {s}')
            df = pd.read_excel(xls, index_col=0, sheet_name=s)
            if "formula" not in df.columns:
                inner.update(1)
                continue
            df['filename'] = os.path.basename(f)
            converter = ce.createInstances(df)
                    
            tableauResult = lambda x: converter.convert(x['formula'], x['datatype'], x['twb'],  x['tds']) if x['column_type'] == "DERIVED" and x['column_id'] not in column_ignore_column_id else ("", 0)
            df[['dax_formula',"require_review"]] = pd.DataFrame(df.apply(tableauResult, axis=1).tolist(), index=df.index)

            if s not in result.keys():
                result[s] = list()
            result[s].append(df)
            inner.update(1)
        outer.update(1)


    with pd.ExcelWriter(outFilename) as writer:
        outer2 = tqdm(total=len(result.keys()), desc='Saving to Excel', position=4)
        sheet_log2 = tqdm(total=0, bar_format='{desc}', position=5)
        for r in result.keys():
            sheet_log2.set_description_str(f'Saving {r}...')
            temp = result[r]
            sheet = pd.concat(temp, ignore_index=True)
            sheet.to_excel(writer, sheet_name=r, index=False)
            outer2.update(1)
