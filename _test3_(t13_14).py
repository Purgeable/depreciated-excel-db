# -*- coding: utf-8 -*-

from markup import Frame
from frame2db import Loader, view_file
from db2xls import write_xls_csv

# Test Excel source file:
# t13_14.xls
# Comment: varnames and data area are on different sheets


# -------------------------
#   Excel file markup
# -------------------------
g = Frame()
g.set_file('t13_14.xlsx')
g.set_sheet('Активы')
g.timeline.set_row(2)
g.data_area.set_start("BV3")
a = g.timeline._sheet.name
g.varnames.set_sheet('разметка')
b = (g.timeline._sheet.name)
g.varnames.set_col('E')
print(g)

# returns empty set:
[x for x in g.timeline.cells]

# b must be equal to a
# g.varnames.set_sheet('разметка') must not 
# alter 'g.timeline._sheet'
# not clear why it does



'''
# -------------------------
#   Read data from Excel
# -------------------------
loader = Loader(h)
loader.execute()

view_file(h._sheet._file.base + '.db3')


# ------------------------------
#   Dump data from db to Excel
# ------------------------------
write_xls_csv('rowdata')
'''


