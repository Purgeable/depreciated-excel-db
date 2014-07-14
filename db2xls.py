import sqlite3
from xlsxwriter.workbook import Workbook
import csv

import global_user_settings as settings
from dir_file import GenericFile
import queries

FIRST_COL_WIDTH = 15
OTHER_COL_WIDTH = 8.5
ROW_HEIGHT = 12.5


def write_xls_csv(basename, varnames=[], date_range={}, by_row=True):
    """

    :param basename: working file name
    :param var_names: list of variables if it's empty get_all_varnames().
    :param date_rage: dict that containd start_date, end_date and table
    :param by_row: True or False set the write data orientation
    :return:
    """
    db_file = GenericFile(basename + '.db3',  dir_type="db3",
                          must_exist=True).fullname
    xl_file = GenericFile(basename + '.xlsx', dir_type="xls_output",
                          must_exist=False).fullname
    csv_file = GenericFile(basename + '.csv', dir_type="csv_output",
                           must_exist=False).fullname


    # open csv
    csv_file_obj = open(csv_file, 'w', newline='')
    csvwriter = csv.writer(csv_file_obj, delimiter=settings.CSV_DELIMITER)

    # open workbook
    workbook = Workbook(xl_file)
    workbook.formats[0].font_name = 'Arial'  # 8.a set font to Arial
    worksheet = workbook.add_worksheet(basename)  # 8.c WorkSheet name as FileName
       
    # add formats for excel cells
    cell_format = workbook.add_format({'font_size': 8, 'font_name': 'Arial'})
    col_header_format = workbook.add_format({'font_size': 8,
                                             'font_name': 'Arial',
                                             'align': 'center'})

    method = 'array_search'

    orientation_1 = 'column'
    orientation_2 = 'row'

    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()

        if not date_range:
            dt = get_all_dates(c)
        else:
            dt = get_dates_by_range(c, **date_range)
        if not varnames:
            varnames = get_all_varnames(c)
            method = 'subquery'
        # set column widths in xls file, uses dt
        worksheet.set_column(0, 0, FIRST_COL_WIDTH)
        worksheet.set_row(0, ROW_HEIGHT)  # 8.b Set row height
        if len(dt) > 0:
            worksheet.set_column(1, len(dt), OTHER_COL_WIDTH)

        # start writing to xls files
        if by_row:
            # write column names
            worksheet.write_row(0, 1, dt, col_header_format)
            # write row names
            worksheet.write_column(1, 0, varnames, cell_format)
        else:
            # write column names
            worksheet.write_row(0, 1, varnames, col_header_format)
            # write row names
            worksheet.write_column(1, 0, dt, cell_format)

        csvwriter.writerow([""] + dt)

        # write data row for each element of varnames
        for i, vn in enumerate(varnames):
            select_var = queries.get_var(c, vn)
            range_values = queries.make_xls_range_values(select_var, dt, method)
            worksheet.set_row(1+i, ROW_HEIGHT)
            if by_row:
                worksheet.write_row(1 + i, 1, range_values, cell_format)
            else:
                worksheet.write_column(1, 1+i, range_values, cell_format)

            # replace '.' by settings.CSV_DEC as a decimal sign 
            csv_row = ["{}".format(x).replace(".", settings.CSV_DEC)
                       for x in range_values]
            csvwriter.writerow([vn] + csv_row)
            
    workbook.close()
    csv_file_obj.close()
    

# get
# SN_1 changed from table = settings.DB_TABLE_RAW
def get_all_dates(c, table=settings.DB_TABLE):
    line = "select distinct dt_string from %s order by 1" % table
    mysel = c.execute(line)
    return([x[0] for x in mysel])


# get varnames
# SN_1 changed from table = settings.DB_TABLE_RAW
def get_all_varnames(c, table=settings.DB_TABLE):
    line = "select distinct varname from %s" % table
    mysel = c.execute(line)
    return([x[0] for x in mysel])


# 7.a date bounderies
def get_dates_by_range(c, start_date, end_date, table=settings.DB_TABLE):
    line = "select distinct dt_string from %s where dt_string >= '%s' " \
           "and dt_string <= '%s' order by 1" % (table, start_date, end_date)
    mysel = c.execute(line)
    return([x[0] for x in mysel])
  
  



