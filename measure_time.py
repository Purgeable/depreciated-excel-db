import time 


def get_func_execution_time(message, func, *args, **kwargs):
    """
    function to measure 'func' execution time and print it
    """
    t = time.process_time()
    func(*args, **kwargs)
    elapsed_time = time.process_time() - t
    print(message, "Process time:", elapsed_time, "seconds")


class MeasureTime():

    def __init__(self, period_name=None):
        self._t = None
        self._period_name = None
        self.periods = [None, None, None]
        self.period_names = ['markup_time', 'frame2db_time', 'db2xls_time']
        if period_name is not None:
            self.start_time(period_name)

    def start_time(self, period_name, push=True):
        if push:
            self.push()
        if period_name not in self.period_names:
            raise Exception('Invalid period name: %s' % period_name)
        self._period_name = period_name
        self._t = time.process_time()

    def push(self):
        if self._t is not None:
            elapsed_time = time.process_time() - self._t
            self.periods[self.period_names.index(self._period_name)] = \
                elapsed_time

    def show(self, push=True):
        if push:
            self.push()
        print('Execution time (in seconds): ', tuple(self.periods))
        return tuple(self.periods)
