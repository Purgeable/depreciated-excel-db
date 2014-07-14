"""test for new plugin"""
import unittest

from markup import Frame


class MarkupTestCase(unittest.TestCase):

    def test_Frame(self):
        # init empty frame
        g = Frame()

        g.set_file('rowdata.xls')
        g.set_sheet(1)
        g.timeline.set_row(2)
        g.varnames.set_col("A")
        g.data_area.set_start("C3")

        self.assertTrue(g.byRow)
        self.assertEqual(g.data_area._sheet.__str__().split("File:\n ")[1],
                         'rowdata.xls\nSheet index (based at 0):\n 0\nSheet name:\n Центральный банк')
        data_list = [x for x in g.data]
        self.assertEqual(len(data_list), 325)
