def data_comp(left, right, method = ['in', 'dict'][0]):
    """Returns a list with  memebers of 'right', which are not part of 'left'
    """
    result = []
    
    if method == 'in':
      for x in right:
        if x not in left:
            result.append(x)
    return(result)

    if method == 'dict':
    # Experimental comparison and diagnostics method    
        errors = {'Different keys':[], 'Keys not found':[], 'Duplicate values':[]}
        dict_a = {}
        dict_b = {}
        for x in left:
            if (x[0], x[1]) not in dict_a.keys():
                dict_a[x[0], x[1]] = x[2]
            else:
                errors['Duplicate values'].append((x[0], x[1], x[2]))
        for y in right:
            dict_b[y[0], y[1]] = y[2]
        for key, data in dict_a.items():
            if key in dict_b.keys():
                if dict_b[key] != data:
                    errors['Different keys'].append((key[0], key[1], data, dict_b[key]))
                    continue
            else:
                errors['Keys not found'].append((key[0], key[1], data))
                continue
        if errors['Different keys'] == [] and errors['Keys not found'] == [] and errors['Duplicate values'] == []:
            return True
        else:
            return errors

    if method == 'some other methonds from stackoverflow links below':    
       '''More concise implementations:
       http://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
       http://stackoverflow.com/questions/16138015/python-comparing-two-lists'''

def find_duplicates(m):
    duplicates = set([x for x in m if m.count(x) > 1])
    return(list(duplicates))

def is_equal(a, b):
    flag0 = (len(a) == len(b)) 
    flag1 = (data_comp(a, b) == [])
    flag2 = (data_comp(b, a) == [])
    if flag0 and flag1 and flag2:
        return(True)
    else:
        return(False)
    
def has_duplicates(m):
    if find_duplicates(m) != []:
        return(True)
    else:
        return(False)

def inspect(a, b):    
    print("\nComparing two arguments...",
            "First argument starts with:", a[0],
            "Second argument starts with:", b[0],
            sep = '\n' )
    
    if len(a) != len(b):
        print("Arguments have different length: {}, {}".format(len(a), len(b)))

    for i, x in enumerate([a, b]):
      if has_duplicates(x):
        print("Argument {} has duplicates of following elements:".format(i))
        for z in find_duplicates(x):
              print(z)

    print("Elements in second argument outside of first argument:")
    for z in data_comp(a, b):
        print(z)

    print("Elements in first argument outside of second argument:")
    for z in data_comp(b, a):
        print (z)
        
    print('''Is 'a' equal to 'b'? ''', is_equal(a, b))



a = [('tag1', '2014-01-01', 100)
   , ('tag1', '2014-02-01', 110)]

b = a

a_dup = a + [a[-1]]

c = [('tag1', '2014-01-01', 100)
   , ('tag1', '2014-02-01', 300)
   , ('tag1', '2014-03-01',  -5)]

d1 = [1]
d2 = d1 * 10

f1 = [1,1,2,2,2]
f2 = [1,1,1,2,2]

   
# Inspection calls:
inspect(a,b)
inspect(a,c)
inspect(d1,d2)
inspect(f1,f2)


# Tests
# todo: extend test, show results ina  more illustrative way
test_result = [ is_equal(a, b) == True
              , is_equal(b, a) == True
              , find_duplicates(a_dup) == [a_dup[-1]]
              , is_equal(d1, d2) == False
              , is_equal(f1, f2) == False
                ]
print('\nPerfoming tests')    
for i, x in enumerate(test_result):
    if x == True:
        print ('Test {} passed'.format(i))
    else:
        print ('Test {} failed'.format(i))



# todo: embed as __eq__ or similar class for Frame()
# comment: find_duplicates() can be a generator, using yield(). Perhaps better for large datasets
# 
