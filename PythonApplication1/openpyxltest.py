from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A4'] = 4
ws['A1'] ='Hello'
#
source = wb.active
target = wb.copy_worksheet(source)

#  4行 2列 写入值 10
cel = ws.cell(row=4,column=2,value=10)

# 创建一行并 再cell中赋值
for row in ws.iter_rows(min_row=2,max_col=4,max_row=2):
    for cell in row:
        cell.value = 'Huiiii'


wb.save('Fir.xlsx')