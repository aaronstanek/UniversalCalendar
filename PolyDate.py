class PolyDate(object):
    def __init__(self,*args,**kwargs):
        raise Exception("Creating an instance of the base class PolyDate is forbidden")
    def __lt__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n < other.universal()._n
        raise TypeError("PolyDate.__lt__ can only be called with a PolyDate instance")
    def __gt__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n > other.universal()._n
        raise TypeError("PolyDate.__gt__ can only be called with a PolyDate instance")
    def __le__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n <= other.universal()._n
        raise TypeError("PolyDate.__le__ can only be called with a PolyDate instance")
    def __ge__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n >= other.universal()._n
        raise TypeError("PolyDate.__ge__ can only be called with a PolyDate instance")
    def __eq__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n == other.universal()._n
        raise TypeError("PolyDate.__eq__ can only be called with a PolyDate instance")
    def __ne__(self,other):
        if isinstance(other,PolyDate):
            return self.universal()._n != other.universal()._n
        raise TypeError("PolyDate.__ne__ can only be called with a PolyDate instance")
    def __add__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("PolyDateDate.__add__ can only be called with an integer")
    def __radd__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("PolyDate.__radd__ can only be called with an integer")
    def __sub__(self,other):
        # other may be an int
        # or may be a PolyDate instance
        if type(other) == int:
            return self._subtract_int(other)
        if isinstance(other,PolyDate):
            return self.universal()._n - other.universal()._n
        raise TypeError("PolyDate.__sub__ can only be called with an integer or PolyDate instance")
    def __iadd__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("PolyDate.__iadd__ can only be called with an integer")
    def __isub__(self,num):
        if type(num) == int:
            return self._subtract_int(num)
        raise TypeError("PolyDate.__isub__ can only be called with an integer")

# all child classes of PolyDate must have the following:

# lower_bound (static variable)
# upper_bound (static variable)
# .universal()
# .number()
# str()
# _addition
# _subtract_int

# child classes may define additional methods