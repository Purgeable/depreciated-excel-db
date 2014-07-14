class NotValidMethodException(Exception):
    """
    Handle Method exceptions
    """
    def __init__(self, method, msg):
        self.method = method
        self.msg = msg
        exception = {'method': method,
                     'msg': msg, }
        Exception.__init__(self, exception)

    def get_msg(self):
        """
        Message from exception
        :return:
        """
        return self.msg
