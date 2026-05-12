import openpyxl
wb = openpyxl.load_workbook(r'C:\Users\geofd\Downloads\Modified_CCRO_pH_Data.xlsx')
ws = wb['pH_Monthly_Summary']

print('All rows:')
for row in ws.iter_rows(min_row=1, values_only=True):
    print(row)
