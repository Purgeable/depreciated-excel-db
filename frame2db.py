import os
import time
import sqlite3
from pprint import pformat, pprint

from dir_file import GenericFile
from markup import Frame
import global_user_settings as settings


class Loader():
    def __init__(self, f, aggregate_duplicate_varnames=False):
        self.queue = []
        self.add(f)
        self._aggregate_duplicate_varnames = aggregate_duplicate_varnames
        
    def add(self, f):        
        if isinstance(f, Frame):
            self.queue.append(f)
        else:
            raise NameError("Argument is not a Frame() class instance")
            
    def get_filename(self): 
        openfile = None
        filenames = [q.data_area._sheet._file.base for q in self.queue] 
        if len(set(filenames)) > 1:
            raise NameError("Frames belong to different files")
        else: 
            fn = filenames[0] + ".db3"
            openfile = GenericFile(fn, dir_type="db3",
                                   must_exist=False).fullname
        return(openfile)

    def execute(self): 
        filename = self.get_filename()
        conn, cursor = start_db(filename)
        for frame in self.queue:
           load_frame(frame, conn, self._aggregate_duplicate_varnames)

        #SN_1 Loader.execute() - aggregation added
        if self._aggregate_duplicate_varnames:
            cursor.execute('''DROP TABLE IF EXISTS %s''' % settings.DB_TABLE)
            line = '''\
CREATE TABLE %s as
SELECT varname, dt_string, sum(value) as value
FROM %s
GROUP BY varname, dt_string
ORDER by 1, 3''' % (settings.DB_TABLE, settings.DB_TABLE_RAW)
            cursor.execute(line)

        conn.commit()
        conn.close()

    #SN_1 Loader Class - properties added
    @property
    def aggregate_duplicate_varnames(self):
        return self._aggregate_duplicate_varnames

    @aggregate_duplicate_varnames.setter
    def aggregate_duplicate_varnames(self, value):
        self._aggregate_duplicate_varnames = value


def create_table(filename):
  conn = sqlite3.connect(filename)
  c = conn.cursor()
  c = c.execute('''DROP TABLE IF EXISTS %s''' % settings.DB_TABLE_RAW)

  c = c.execute('''CREATE TABLE %s (
	varname VARCHAR(256) NOT NULL,
	dt_string DATE NOT NULL,
	value FLOAT NOT NULL)''' % settings.DB_TABLE_RAW)

  #SN_1 create final table for loading if _aggregate_duplicate_varnames==False
  c = c.execute('''DROP TABLE IF EXISTS %s''' % settings.DB_TABLE)
  c = c.execute('''CREATE TABLE %s (
	varname VARCHAR(256) NOT NULL,
	dt_string DATE NOT NULL,
	value FLOAT NOT NULL)''' % settings.DB_TABLE)

  conn.commit()

  #c.execute('''PRAGMA table_info('%s')''' % settings.DB_TABLE_RAW)
  #oevre = c.fetchall()
  #print(oevre)

  #c.execute('''SELECT * FROM sqlite_master WHERE type='table' ''')
  #oevre = c.fetchall()
  #print(oevre)

  conn.close()


def start_db(filename):
    # if database file not found, create it

    #SN_1 must create tables, even if database file already exists,
    #it may not contain some tables
    # if not os.path.isfile(filename):
    create_table(filename)

    # open database
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("delete from %s" % settings.DB_TABLE_RAW)
    # SN_1 empty final table
    c.execute("delete from %s" % settings.DB_TABLE)
    conn.commit()
    return(conn, c)

def load_frame(frame, conn, aggregate_duplicate_varnames):
    cursor = conn.cursor()
    print ("Inserting data...")

    #SN_1 choose target table using aggregate_duplicate_varnames flag
    target_table_name = settings.DB_TABLE_RAW if aggregate_duplicate_varnames \
        else settings.DB_TABLE
    for vn, dt, x in frame.data:
      line = ("INSERT INTO {0} (varname, dt_string, value) " 
              "VALUES (\'{1}\', \'{2}\', {3})").format(target_table_name,
                                                       vn, dt, x)
      print(line)                                                       
      cursor.execute(line)
     
    # Pause to allow sqlite to finish its job
    DELAY = 1
    print('Inserting complete. Pausing for %s sec...' % DELAY)
    time.sleep(DELAY)

# EP_1 view_file default arg changed from  table = 'temp_table'
def view_file(fn, table = settings.DB_TABLE):
    dbf = GenericFile(fn, dir_type='db3').fullname    
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute('''SELECT * from %s''' % table)
    z = c.fetchall()
    conn.close()
    print ("Filename:", fn)
    print ("Datapoints:", len(z))
    pprint (z)

   

