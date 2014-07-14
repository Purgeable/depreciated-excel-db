import os
import sys
import global_user_settings as settings


DIR_MAP = {
    'xls_source': settings.SOURCE_XLS,
    'csv_output': settings.OUTPUT_CSV,
    'xls_output': settings.OUTPUT_XLS,
    'db3': settings.DB3
}


def nargs(*args):
    return len([x for x in args if x not in ['', None]])


class Directory():
    """Path definition, with respect to user-defined subdirectories
    Arguments:
      basedir - path to main working directory (e.g. "D:/work/excel-db"),
                default value is the directory of this .py file
      subdir  - subdirectory (e.g. 'xls_source', 'db3')
      type    - type of subdirectory:
                'xls_source':global_user_settings.SOURCE_XLS,
                'csv_output':global_user_settings.OUTPUT_CSV,
                'xls_output':global_user_settings.OUTPUT_XLS,
                       'db3':global_user_settings.DB3,
              'txt_settings':global_user_settings.(to be defined)              
    Attributes:
      path    - full directory path (basedir + subdir, example: "D:/work/excel-db/db3")
    Methods:
      set_path(basedir, subdir)
      get_path()"""
         
    @staticmethod
    def check_dir(path):
        if not os.path.exists(path):
            raise IOError("Directory %s does not exist" % path)

    def __init__(self, basedir=None, subdir='', dir_type=None):
        if nargs(basedir, subdir) > 0 and dir_type is not None:
            print (nargs(basedir, subdir))
            raise ValueError("Too many arguments")
     
        if dir_type is not None:
            self._set_by_type(dir_type)
        else:
            self.set_path(basedir, subdir)

    def _set_by_type(self, dir_type):

        if dir_type not in DIR_MAP:
            raise ValueError("Provided subdirectory type not supported")
          
        self.set_path(subdir=DIR_MAP[dir_type])

    def set_path(self, basedir=None, subdir=''):
        # EP_1 self.basedir was not set before, need to use this function code
        
        # set path to where this python File is
        default_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

        # 'basedir': if no path is provided as arguement - use 'default_dir'
        # as 'basedir'
        if basedir is None:
            self.basedir = default_dir
        else:
            self.basedir = basedir
        self.check_dir(self.basedir)

        # 'subdir': pass
        self.subdir = subdir

        # 'basedir' + 'subdir'
        self.path = os.path.join(self.basedir, self.subdir)
        self.check_dir(self.path)

    def get_path(self):
        return self.path

    def __repr__(self):
          return (str(self.path))

    def __str__(self):
          return " ".join(["Path:", self.path])


class GenericFile(Directory):
    """Path definition, with respect to user-defined subdirectories
    Arguments:
     filename    
     must_exist  - True if the file must exist
     obj_dir     - Directory() instance     
     type        - type of subdirectory, as in Directory class.
                   Either 'obj_dir' or 'type' can be supplied.      
    Attributes:
     path     
     filename = base + ext 
     base  
     ext 
     fullname = os.path.lion(path, filename)
     
    Methods:
     set_path(basedir, subdir)
     get_path()
     get_filename()"""

    @staticmethod
    def check_file(fn):
        if not os.path.isfile(fn):
            raise IOError("File %s does not exist" % fn)    

    def __init__(self, filename, dir_type=None, must_exist=False,
                 obj_dir=None):
        # initialize path
        if isinstance(obj_dir, Directory):
            Directory.__init__(self, basedir=obj_dir.basedir,
                               subdir=obj_dir.subdir)
        else:
            Directory.__init__(self, dir_type=dir_type)
        # initialize filename
        if filename is not None:
            self._set_file(filename, must_exist)
            
    def _set_file(self, filename, must_exist=False):        
        self.filename = filename
        self.base, self.ext = os.path.splitext(filename)
        self.fullname = os.path.join(self.path, self.filename)
        if must_exist:
            self.check_file(self.fullname)

    def set_file(self, filename, must_exist=False):        
        self._set_file(filename, must_exist)

    def get_filename(self):
        return str(self.fullname), str(self.path), str(self.filename),
        str(self.base), str(self.ext)

    def __repr__(self):        
          return (str(self.fullname))
        
    def __str__(self):
        return "Filename: %s" % self.fullname

