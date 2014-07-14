## Intro
### Excel-db allows to:
read time series data from Excel files into database (e.g. sqlite, mysql) according to user-defined markup of Excel file
write time series data from a database into csv and xlsx files
Directory structure contains folders for source, output files and sqlite databases. Basic documentation in documentation\pydoc_html folder.
Execution control shown in _test*.py files. Currently only _test0.py and _test1_row.py work properly.

### Tasks in this project stage
#### Overall
1. Short Q&A about program design, several comments along the code, where most questionable
2. Measure execution time in  _test*.py files. Store as tuple of three values (markup_time, frame2db_time, db2xls_time)
markup.py

3. Enhance code in Cell.set_cell

4. _test3_(t13_14).py fails. Need working functionality to set Frame().varnames._sheet independently of  timeline._sheet and data_area._sheet
frame2db.py
5. _test2_col.py writes longer time-series to several variables in colnames.xlsx. See explaination and to-do pseudocode.
db2xl.py
6. Propose refactoring db2xl module considering tasks below. After approved, implement it.
7. Boundaries
a. limit output to dates between start_date and end_date, if not supplied, use get_all_dates(). # Done
b. limit output to a list ‘user_specified_vars’, e.g.  =  [‘cb.a.row’, ‘cb.p.row’] # Done
c. propose format to store user-defined date limits and variable list
8. Excel sheet formatting  # Done
a. sheet should not have Calibri font – all in Arial # Done
b. set row height to 12,75 # Done
c. name sheet same as filename # Done
9. Оption to write data by row of by column byRow = True | False # Done
10. Make make_xls_range_values return an iterable and take METHOD as an argument # Done
11. Review ‘queries.py’ # Done
