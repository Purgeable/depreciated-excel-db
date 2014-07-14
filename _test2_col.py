# -*- coding: utf-8 -*-
from markup import Frame
from frame2db import Loader, view_file
from db2xls import write_xls_csv

# Test Excel source file:
# coldata.xls
fn_base = 'coldata'

# Reads data by column
# The source data file contains same tags at different
# columns. These columns need to be summed.


# Required pseudocode in frame2db.py:
# Introduce flag aggregate_duplicate_varnames = False
# if aggregate_duplicate_varnames = False: # (default)
#    read data into table settings.DB_TABLE
# if aggregate_duplicate_varnames = True:
#    read data into table settings.DB_TABLE_RAW
#    aggregate data into settings.DB_TABLE_RAW
#        adjust for current fields 
#        line = '''CREATE TABLE %s as SELECT varname, dt_string, sum(value) as value
#        FROM %s GROUP BY varname, dt_string, dt_julian ORDER by 1, 3''' % (p.DB_TABLE, p.DB_TABLE_RAW)
#        c.execute(line)

# Required changes in markup or loader:
#     store and pass 'aggregate_duplicate_varnames' flag
#     the flag affect all queue, but may be stored at markup level
#
# Required changes in db2xls:
#     read from settings.DB_TABLE, not settings.DB_TABLE_RAW

# -------------------------
#   Excel file markup
# -------------------------
h = Frame()
h.default_markup(fn_base + '.xls', sheet = 2, byRow = False)
print(h)

# -------------------------
#   Read data from Excel
# -------------------------
loader = Loader(h)
loader.execute()

# view_file(h._sheet._file.base + '.db3')


# ------------------------------
#   Dump data from db to Excel
# ------------------------------
write_xls_csv(fn_base)

