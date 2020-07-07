class PolyDate(object):
    def __init__(self,*args,**kwargs):
        raise Exception("Creating an instance of the base class PolyDate is forbidden")

# all child classes of PolyDate must have the following:

# .universal()
# str()
# + int
# int +
# - int
# - PolyDate
# += int
# -= int

# child classes may define additional methods