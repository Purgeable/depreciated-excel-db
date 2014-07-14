# -*- coding: utf-8 -*-
import global_user_settings as p
from api_exceptions import *

METHOD = ('array_scan', 'array_search', 'subquery',)

# get variable values for all existing dates
def get_var(c, v, method='subquery'):
    if method not in METHOD:
        raise NotValidMethodException(method, 'Method not found')
    if method == 'subquery':
        return get_var_subquery(c, v)
    else:
        return get_var_array(c, v)


# get variable values for all existing dates
# for METHODs: 'array_scan', 'array_search'
def get_var_array(c, v):
    #SN_1 use final table instead of temp
    line = '''select varname, dt_string, value from %s ''' % p.DB_TABLE + \
        ''' where varname = '%s' order by dt_string''' % v
    mysel = c.execute(line)
    return(mysel.fetchall())


# get variable values for all existing dates
# if a variable values is missing for specific date it is assigned NULL
# for METHOD: 'subquery'
def get_var_subquery(c, v):
    #SN_1 use final table instead of temp
    line = '''\
    select '{1}' as varname, a.dt_string, b.value
    from
        (select distinct dt_string from {0}) a
        left outer join
        (select dt_string, sum(value) as value
         from {0}
         where varname = '{1}'
         group by dt_string) b
        on a.dt_string = b.dt_string
    order by a.dt_string'''.format(p.DB_TABLE, v)
    mysel = c.execute(line)
    return(mysel.fetchall())


# use make_xls_range_values_[subquery|array_scan|array_search] for actual work
def make_xls_range_values(select_var, dt, method='subquery'):
    if method not in METHOD:
        raise NotValidMethodException(method, 'Method not found')
    return globals()['make_xls_range_values_%s' % method](select_var, dt)


# filter selection with respect for dates in query
# for method: 'subquery'
def make_xls_range_values_subquery(select_var, dt):
    # substitute NULL is selection with p.XLS_NA
    xls_range_values = [x[2] if x[2] is not None else p.XLS_NA
                        for x in select_var]
    return(xls_range_values)


# filter selection with respect for dates in query
# for method: 'array_scan'
def make_xls_range_values_array_scan(select_var, dt):
    # timelines in query and in selection are compared by length
    if len(select_var) == len(dt):
        # write entire selection from database
        xls_range_values = [x[2] for x in select_var]
    else:
        select_index = 0 # индекс текущего элемента в select_var
        xls_range_values = []
        for dateval in dt:
            if select_index < len(select_var):
                select_var_item = select_var[select_index]
                select_dateval = select_var_item[1]
                if dateval == select_dateval:
                    xls_range_values.append(select_var_item[2])
                    select_index += 1
                    continue
            xls_range_values.append(p.XLS_NA)
    return(xls_range_values)


# filter selection with respect for dates in query
# for method: 'array_search'
def make_xls_range_values_array_search(select_var, dt):
    cur_val = p.XLS_NA
    select_var_dates = [x[1] for x in select_var]
    xls_range_values = []

    # timelines in query and in selection are compared by contents
    if set(select_var_dates) == set(dt):
        # write entire selection from database
        xls_range_values = [x[2] for x in select_var]
    else:
        # вызываем обработчик
        # For each date in dt find value in select_var.
        # If not found, use p.XLS_NA
        for d in dt:
                # for each date in dt choose values from select_var
            if d in select_var_dates:
                cur_val = [x[2] for x in select_var if x[1] == d][0]
                xls_range_values.append(cur_val)
            else:
                # if this date is not in select_var - write XLS_NA
                cur_val = p.XLS_NA
                xls_range_values.append(cur_val)

    return(xls_range_values)
