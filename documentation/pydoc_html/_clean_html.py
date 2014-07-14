import sys

fn = sys.argv[1]

with open(fn, 'r') as fin:
  starts = []
  ends = []
  all_lines = fin.readlines()
  for i, line in enumerate(all_lines):
      if line.startswith("Data descriptors"):
          starts.append(i)
      if "list&nbsp;of&nbsp;weak" in line:
          ends.append(i)
          
  outs = []
  for k in ends[::-1]:
     del all_lines[k-6:k+1]

with open(fn, 'w') as fout:
    fout.writelines(all_lines)
  

