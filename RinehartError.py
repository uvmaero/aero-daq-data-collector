class RinehartException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class RinehartError(RinehartException):
    def __init__(self,*args,**kwargs):
        RinehartException.__init__(self,*args,**kwargs)

