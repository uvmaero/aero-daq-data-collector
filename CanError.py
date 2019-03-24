class CanException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class CanError(CanException):
    def __init__(self,*args,**kwargs):
        CanException.__init__(self,*args,**kwargs)

