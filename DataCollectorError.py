class DataCollectorException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class DataCollectorError(DataCollectorException):
    def __init__(self,*args,**kwargs):
        DataCollectorException.__init__(self,*args,**kwargs)