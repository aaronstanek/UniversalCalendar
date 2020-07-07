class PolyDate(object):
    def __init__(self,*args,**kwargs):
        raise Exception("Creating an instance of the base class PolyDate is forbidden")
    def __lt__(self,other):
        return self.universal()._n < other.universal()._n
    def __gt__(self,other):
        return self.universal()._n > other.universal()._n
    def __le__(self,other):
        return self.universal()._n <= other.universal()._n
    def __ge__(self,other):
        return self.universal()._n >= other.universal()._n
    def __eq__(self,other):
        return self.universal()._n == other.universal()._n
    def __ne__(self,other):
        return self.universal()._n != other.universal()._n

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