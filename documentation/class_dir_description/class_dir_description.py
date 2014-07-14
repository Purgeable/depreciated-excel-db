from dir_file import *
from markup   import *
#from frame2db_classes import *
#from db2xls_classes   import *

FILENAME = 'class_dir_description.txt'

def p(x):
    print(x, file = f)
    print(x)

class_list = [
 Directory(),
 GenericFile('nofile'),
 XlsSourceFile('nofile', must_exist = False),
 Sheet(),
 Position(),
 Cell(),
 Block(), 
 Timeline(),
 Vector(),
 Frame()]

with open(FILENAME, 'w') as f:
 for y in class_list:
  p(y.__class__.__name__)
  for x in dir(y):
    if not "__" in x:
      p("." + x)

