# -*- coding: utf-8 -*-
from markup import Frame
from frame2db import Loader, view_file
from db2xls import write_xls_csv

# Test Excel source file:
# rowdata.xls

# -------------------------
#   Excel file markup
# -------------------------
h = Frame()
h.default_markup('rowdata.xls', 1, byRow = True)
h.data_area.set_end('J21')
print(h)


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


