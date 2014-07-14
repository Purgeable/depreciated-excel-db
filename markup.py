   # -*- coding: UTF-8 -*-

"""
xl2db project
Reads time series data from Excel files into database (e.g. sqlite, mysql) according to user-defined markup of Excel file.

Class Frame

Class contains Excel file markusettings. The markup specifies location of required data in Excel file.

Class Frame defines three cell ranges: 
  timeline (row or column);
  variable names (column or row);
  data area (upper-left cell of the data range, and, optionally, lower-right cell).  

Example:
 
from markup import *
g = Frame()
g.set_file('rowdata.xls')
g.set_sheet(1)
g.timeline.set_row(2)        # required
g.varnames.set_col("A")      # required
g.data_area.set_start("C3")  # required
g.data_area.set_end("H12")   # optional
print(g)

h = Frame()
h.default_markup('rowdata.xls', 1, byRow = True)
print(h)

Comments:
- Default path for data source Excel files is 'xls_source' subdirectory. 
- There can be several frames related to one Excel file.
- If timeline is in row, variable names should be in column and vice versa.
- Timeline and data area must be on the same Excel sheet.
- Data source Excel files usually contain timeline and data area, while variable names (tags) need to be added manually. 
They can be added on the same sheet, or at the same positions on different sheet or even in a different file. Keeping 
variable names separate from data area is sometimes more convenient for updating information.   
- Frame data can be accessed by using data.property, e.g. [x for x in my_frame.data]
"""

import re
from pprint import pformat
import datetime
# EP_1 added copy import
import copy

import xlrd
import xlsxwriter.utility
import types
from dir_file import *

STR_OFFSET = " "
CHAR_SET = 'utf-8'


def newlineprint(*args):
    text = args[0::2]
    x = args[1::2]
    a = []
    for t1, t2 in zip(text, x):
        a.append(t1)
#        if isinstance(t2, unicode):
#            t2 = t2.encode(CHAR_SET)
#        else:
        t2 = str(t2)
        a.append(STR_OFFSET + t2)
    msg = "\n".join(a)
    return(msg)


class XlsSourceFile(GenericFile):
    """*** Excel filename and file/path validity check.
       Argument:
        filename - Excel filename 
        obj_dir - instance of Directory class 
       Attributes:
        fullname - full Excel file path and filename, can be passed to open()
       Public methods:
        set_file(filename)
        get_filename() 
       Property:
        book - xlrd.Book object"""

    def __init__(self, filename, must_exist=True): 
        GenericFile.__init__(self, filename, dir_type='xls_source',
                             must_exist=must_exist)
        # reset xlrd pointer
        self._book = None
    
    def get_book(self):
        """Get xlrd workbook object. Use lazy initialization (i.e. only when
        needed and only once)
        """
        # call _open_book() only on the first call of get_book()
        if self._book is None:
            self.check_file(self.fullname)
            self._book = xlrd.open_workbook(self.fullname)
        # always return same Excel book pointer after first call
        return self._book

    book = property(get_book)


class Sheet():
    """Excel worksheet.
       Inputs:
          obj_file - File object
          idx - zero-based index of Sheet
          idn - 1-based index of Sheet
          name - name of Sheet
        Ouput:
          sheetx - zero-based sheet index
        Property:
          sheet - xlrd worksheet object
    """
    def __init__(self, idn=None, idx=None, name=None, filename=None,
                 obj_file=None):
        self._init_file(filename, obj_file) 
        self._init_sheet(idn, idx, name)

    def _init_file(self, filename, obj_file):
        self._file = XlsSourceFile('nofile', must_exist=False)  # ***
        if not (obj_file is None):  # or isinstance(obj_file, FileType):
            self._file = obj_file            
        if filename is not None: 
            self._file = XlsSourceFile(filename) 
        
    def _init_sheet(self, idn, idx, name):    
        if nargs(idx, idn, name) > 1: 
            raise NameError("Too many arguments")
 
        self.sheetx = 0
        if name is not None:
            self._set_sheet_name(name)
        elif idn is not None:
            self._set_sheet_index_base1(idn)
        elif idx is not None:
            self._set_sheet_index_base0(idx)
            
    def _set_sheet_by_name(self, name):
        try:
            self.sheetx = xlrd.open_workbook(self._file.fullname).\
                sheet_names().index(name)
        except ValueError:
            raise Exception("No Excel sheet named <{}>"
                            " in {}".format(name, self._file.fullname))
            
    def _set_sheet_index_base0(self, idx):        
        if idx in range(xlrd.open_workbook(self._file.fullname).nsheets): 
            self.sheetx = idx
        else: 
            raise Exception("Sheet index <{}> out of bounds" 
                            " in <{}> ".format(idx, self._file.fullname))

    def _set_sheet_index_base1(self, z):
        self._set_sheet_index_base0(z - 1)
        
    def _set_sheet(self, x):
        if isinstance(x, str):
            self._set_sheet_by_name(x)
        elif isinstance(x, int):
            self._set_sheet_index_base1(x)
        else:
            raise Exception("Sheet name or index has wrong type" 
                            "in <{}> ".format(self._file.fullname))

    # public setter method can address sheet by name or index based at 1                            
    # _set_sheet and set_sheet are need to do some overloading in Frame() class
    def set_sheet(self, x):
        self._set_sheet(x)

    def get_sheet(self):
        if self.sheetx is None:
            raise Exception("Error: Sheet is not specified.")
        if self._file is None:
            raise Exception("Error: File is not specified.")
        book = self._file.book
        return book.sheet_by_index(self.sheetx)

    sheet = property(get_sheet)
    
    def get_name(self): 
        book = self._file.book
        name = book.sheet_names()[self.sheetx]
        return (name)
        
    name = property(get_name)
    
    def set_file(self, filename):
        self._file.set_file(filename)
        
    def __repr__(self):        
        return(self._file.fullname + " Sheet (based at 0): <%s>" % self.sheetx)

    # EP (11:06 14.07.2014 MOW)    
    def repr_as_tuple(self):
        result = (                  ("Path", self._file.path),
                                    ("File", self._file.filename),
                ("Sheet index (based at 0)", self.sheetx),
                              ("Sheet name", self.name))   
        return(result)
    
    def repr_as_dict(self):  
        result = {x:y for x,y in self.repr_as_tuple()}
        return(result)

    def _format_repr(self):
    # _format_repr() has to be recycled - as global function, similar to newlineprint()
        result = ""
        for (key, value) in self.repr_as_tuple():
            current_line = key + ": \n" + STR_OFFSET  + str(value)
            result = result + '\n' + current_line
        return(result)
        
    def __str__(self):    
        msg = self._format_repr()
        return(msg)

    '''# will be omitted:      
    def __str__(self):
        msg = newlineprint("Path:", self._file.path,
                           "File:", self._file.filename,
                           "Sheet index (based at 0):", self.sheetx,
                           "Sheet name:", self.name)
        return(msg)
    '''
    
    # To see output:
    # a = Sheet(); a._file.set_file('rowdata.xls'); a._format_repr(); print(a)
    # To test (example):
    # d = a.repr_as_dict(); d['File']=='rowdata.xls' 
   
    # end EP (12:05 14.07.2014 MOW)  

class Position():
    """This class provides methods to set position for a row or a column. 
       Position is stored as an index based at 0.
    """       
    def __init__(self, x=None):
        self.positionx = x
        
    def _set_base0(self, x):
        self.positionx = x
        
    def _set_base1(self, x):
        self.positionx = x - 1
        
    def _set_letter(self, lettername):
        _proxy_cell = lettername.upper() + '1'
        self.positionx = xlsxwriter.utility.xl_cell_to_rowcol(_proxy_cell)[1]
                
    def _set(self, x):
        if isinstance(x, str):
            self._set_letter(x)
        elif isinstance(x, int):
            self._set_base1(x)
        else:
            # Should this be ValueError?
            raise ValueError("Wrong argument type")
    
    def _get_positionx(self):
        return self.positionx
    
    x = property(_get_positionx, _set_base0)


class Cell():
    """
    Excel cell
    """
    def __init__(self, rowx=None, colx=None):
        self.rowx = rowx
        self.colx = colx
        
    def set_cell(self, x):  
          """Must accept 'a1', 'A1', 1, 'A', "AB", 'ab' as arguments
          """
          if isinstance(x, str):    
              apart = None  # letter part of a1-style reference
              npart = None  # numeric part of a1-style reference          
              
              #SN_1 shorter version
              search_result = re.search("^(\D*)(\d*)$", x)
              if search_result is not None:
                apart = search_result.group(1)
                npart = search_result.group(2)
              # ***
              
              if apart and npart:
                  a1ref = apart.upper() + npart
                  self.rowx, self.colx = xlsxwriter.utility.xl_cell_to_rowcol(a1ref)              
              elif npart:
                  rowx = int(npart)              
              elif apart:
                  _proxy_cell = apart.upper() + '1'
                  self.colx  = xlsxwriter.utility.xl_cell_to_rowcol(_proxy_cell)[1] 
          elif isinstance(x,int):
              self.rowx = x - 1 
       
    def _get_cell_address(self):
        return(xlsxwriter.utility.xl_rowcol_to_cell(self.rowx, self.colx))
        
    def __str__(self):
      if self.rowx is not None and self.colx is not None:
        a1_style_ref = self._get_cell_address()
      else:
        a1_style_ref = 'undefined' 
      msg = newlineprint("Cell row (based at 0):", self.rowx, 
                         "Cell column (based at 0):", self.colx,
                         "Cell address:", a1_style_ref)     
      return(msg)
        

class Block():
    """Cell range
    """    
    def __init__(self):
       self.start = Cell()
       self.end = Cell()
       self._sheet = Sheet()
       
    def set_start(self, a1ref):
      self.start.set_cell(a1ref)
      
    def set_end(self, a1ref):
      self.end.set_cell(a1ref)   
  

    def set_range(self, double_a1ref):
      ref1, ref2 = re.search("(.+):(.+)", double_a1ref).group(1,2)
      self.start.set_cell(ref1)
      self.end.set_cell(ref2)
      
    def __str__(self):
        msg = "\n".join(['Upper-left cell',
                         self.start.__str__(),
                         "\nLower-right cell",
                         self.end.__str__()])         
        return(msg)     

      
class Vector(Position):
    """Dual class for a row or column cooxlrdinate. 
       Vector().type string indicates orientation ('row', 'col').
    """
    def __init__(self, rowx=None, colx=None, sheet_obj = None):
    
        positionx = None
        if rowx is not None and colx is None: 
           self.type = 'row'; positionx = rowx
        elif rowx is None and colx is not None:
           self.type = 'col'; positionx = colx
        else: self.type = None        
        Position.__init__(self, positionx)
        
        self.start = Position()
        self.end = Position()
        
        if isinstance(sheet_obj, Sheet): 
           self._sheet = sheet_obj
        else: self._sheet = None

    def set_col(self, x):
       if x is not None:
          self._set(x)
          self.type = 'col'

    def set_row(self, x):
       if x is not None:       
          self._set_base1(x)
          self.type = 'row'

    def set_end(self, x):
        self.end._set(x)

    def set_start(self, x):
        self.start._set(x)
        
    def set_vector_sheet(self, x):
        self._sheet.set_sheet(x)
        
    def set_sheet(self, x):
        self._sheet.set_sheet(x)
       
    def next_val(self):
        sh = self._sheet.sheet
        startx = self.start.positionx 
        endx = self.end.positionx 
        if self.type == 'row':
            t = sh.row_values(self.positionx, start_colx=startx, end_colx=endx)
#       extract = sh.row_values
        if self.type == 'col':
            t = sh.col_values(self.positionx, start_rowx=startx, end_rowx=endx)
#       extract = sh.col_values
#       extract(self.positionx, startx, endx)
#       extract() is an alternative call for  row_values(), col_values()
       
        for i, x in enumerate(t):
          if x != '': 
            if self.type == 'row':          
              z = (self.positionx, i + startx, x)
            if self.type == 'col': 
              z = (i + startx, self.positionx, x)            
            yield(z)
     
    cells = property(next_val)

    def __str__(self):
        a = {'row':['Row (based at 0):', 'column'],
             'col':['Column (based at 0):', 'row']}
        i = self.type 
        if i != 'undefined':
          msg = newlineprint(a[i][0], self.positionx, 
                           'First element at '+a[i][1]+" (based at 0):", self.start.x,
                           'Last element at '+a[i][1]+" (based at 0):", self.end.x) 
        else: msg = "Orientation undefined"   
        msg = "\n".join([self._sheet.__str__(), msg])
        return (msg)       


class Timeline(Vector):
    def __init__(self):
        Vector.__init__(self)
        self._sheet = None 
    
    @staticmethod
    def time_cells_filter(x):     
            if isinstance(x, str):
                if len(x.strip()) == 0:
                    return (None)
                # string representation of date
                return (x)
            elif abs(float(int(x)) - x) < 1e-10 and 1800 < x < 4000:
                # integer year
                return (str(int(x)))
            else:
                # date in excel format
                return(
                    datetime.date(*xlrd.xldate_as_tuple(x, 0)[0:3]).__str__())
                 
    def get_timeline(self):
        """Get list of dates from timeline row/col
        """
        for (rowx, colx, val) in self.next_val():
            modif_val = self.time_cells_filter(val)
            result = (rowx, colx, modif_val)
            yield (result)

    cells = property(get_timeline)


class Frame:
    def __init__(self):
        self._sheet = Sheet()
        self.timeline = Timeline()        
        self.varnames = Vector()
        self.data_area = Block()
        self.byRow = True
   
    def set_path(self, basedir=None, subdir=''):
        # EP_1 code was omitted before
        self._sheet._file.set_path(basedir = basedir, subdir = subdir)    
        
    def set_file(self, filename):
        if filename is not None:
            self._sheet.set_file(filename)
        
    def set_sheet(self, x):
        if x is not None:
            self._sheet._set_sheet(x)
        else:
            self._sheet._set_sheet(1)        
        self._replicate_sheets()

    def _replicate_sheets(self):
        #SN_1, EP_1 timeline and data_area sheet will point to default sheet
        self.timeline._sheet = self._sheet
        self.data_area._sheet = self._sheet
        
        #SN_1 copy objects instead of reference to avoid overwrite same object         
        self.varnames._sheet = copy.copy(self._sheet)
        
    def _pass_limits(self):
        start_rowx = self.data_area.start.rowx
        start_colx = self.data_area.start.colx
        end_rowx = self.data_area.end.rowx
        end_colx = self.data_area.end.colx
         
        if self.byRow == True:
          self.varnames.start.x = start_rowx
          self.varnames.end.x = end_rowx
          self.timeline.start.x = start_colx
          self.timeline.end.x = end_colx    
        
        else:        
          self.varnames.start.x = start_colx
          self.varnames.end.x = end_colx
          self.timeline.start.x = start_rowx
          self.timeline.end.x = end_rowx        
        
    def _apply_markup(self, filename=None, sheet=None, byRow = True): 
      self.set_file(filename)
      self.set_sheet(sheet)
      self.byRow = byRow
      if self.byRow == True:
        self.timeline.set_row(2)
        self.varnames.set_col("A")
        self.data_area.start.set_cell("C3")
      else:
        self.timeline.set_col("A")
        self.varnames.set_row(1)
        self.data_area.start.set_cell("B3")
      self._pass_limits()

    def default_markup(self, filename=None, sheet=None, byRow = True): 
    # Default markup currently set to 'byRow=True', will be changed to byRow=False
       self._apply_markup(filename, sheet, byRow)
       
    def next_data(self):
      self._pass_limits()
      sheet = self.data_area._sheet.sheet      
      for (vn_rowx, vn_colx, vn_val) in self.varnames.cells:
        for (dt_rowx, dt_colx, dt_val) in self.timeline.cells:
          if self.byRow == True:
            rowx = vn_rowx
            colx = dt_colx
          else:
            rowx = dt_rowx
            colx = vn_colx        
          data_val = sheet.cell_value(rowx, colx)
          result = (vn_val, dt_val, data_val)
          yield(result)
   
    data = property(next_data)

    def validate(self):
        """ todo: need more tests and validation rules 
        """
        if self._default_sheet._file is None:
            raise Exception("Default Sheet _file not specified")
        if self._default_sheet.sheetx is None:
            raise Exception("Sheet index is not specified for default Sheet")
        if self.timeline.rowx is None:
            raise Exception("timeline.rowx not specified")
        if self.varnames.colx is None:
            raise Exception("varnames.colx not specified")
        if self.values.start.rowx is None:
            raise Exception("value_area.start.rowx not specified")
        if self.values.end.rowx is None:
            print ("Warning: value_area.end.rowx not specified")
        if self.values.start.colx is None:
            raise Exception("value_area.start.colx not specified")
        if self.values.end.colx is None:
            print ("Warning: value_area.end.colx not specified")
            
    def __str__(self):    
       #*** 'first n given'
       data_list = [x for x in self.data]       
       msg = "\n".join([
         self.data_area._sheet.__str__(),
         "Timeline:",
         pformat([x for x in self.timeline.cells]),
         "Variable names:",
         pformat([x for x in self.varnames.cells]),
         "Datapoints (total {} datapoints):".format(len(data_list)),
         pformat(data_list) ])
         
       return(msg)
