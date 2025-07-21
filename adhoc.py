import pandas as pd
from tqdm import tqdm

outFile = 'dump/combined.xlsx'
sheets = ['table','column','bin','list_table','Summary']
files = [
    'Batch_1_Analysis_Combined.xlsx', 
    'Batch 2_Reports 51-205.xlsx',
    'Batch 2_First 50 reports.xlsx', 
    '16_April Report_Analysis.xlsx',
    ]
result = dict.fromkeys(sheets)

if __name__ == '__main__':
    outer = tqdm(total=len(files), desc='Files', position=0)
    file_log = tqdm(total=0, bar_format='{desc}', position=1)
    sheet_log = tqdm(total=0, bar_format='{desc}', position=2)
    for f in files:
        inner = tqdm(total=len(sheets), desc='Sheets', position=3)
        file_log.set_description_str(f'Current file: {f}')
        xls = pd.ExcelFile(f)
        for s in sheets:
            sheet_log.set_description_str(f'Current sheet: {s}')
            df = pd.read_excel(xls, index_col=0, sheet_name=s)
            df['filename'] = f
            if not result[s]:
                result[s] = []
            result[s].append(df)
            inner.update(1)
        outer.update(1)


    with pd.ExcelWriter(outFile) as writer:
        outer2 = tqdm(total=len(result.keys()), desc='Saving to Excel', position=4)
        sheet_log2 = tqdm(total=0, bar_format='{desc}', position=5)
        for r in result.keys():
            sheet_log2.set_description_str(f'Saving {r}...')
            temp = result[r]
            sheet = pd.concat(temp, ignore_index=True)
            sheet.to_excel(writer, sheet_name=r, index=False)
            outer2.update(1)
