from markup import *

# init empty frame
g = Frame()

g.set_file('rowdata.xls')
g.set_sheet(1)
g.timeline.set_row(2)
g.varnames.set_col("A")
g.data_area.set_start("C3")
# shorter code for above:
g.default_markup('rowdata.xls', 1, byRow = True)

g.timeline.set_start("C")
g.timeline.set_end("H")
g.varnames.set_start(3)
g.varnames.set_end(12)
# shorter code for above:
g.data_area.set_start("C3")
g.data_area.set_end("H12")
# or even shorter:
g.data_area.set_range("C3:H12") 
print(g)
