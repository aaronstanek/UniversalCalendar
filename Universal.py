from .PolyDate import PolyDate

class UniversalDate(PolyDate):
    # _n is the universal date number
    # universal date zero is 1 Jan of the year -1
    # in the proleptic Gregorian system
    def __init__(self,other):
        if type(other) == int:
            self._n = other
            return
        if isinstance(other,PolyDate):
            other_universal = other.universal()
            self._n = other_universal._n
            return
        raise TypeError("UniversalDate can only be constructed from an integer or PolyDate instance")
    def universal(self):
        return self
    def __str__(self):
        return "UniversalDate(" + str(self._n) + ")"
    def _addition(self,num):
        # num must be an integer
        return UniversalDate(self._n + num)
    def __add__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("UniversalDate.__add__ can only be called with an integer")
    def __radd__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("UniversalDate.__radd__ can only be called with an integer")
    def _subtract_int(self,num):
        # num must be an integer
        return UniversalDate(self._n - num)
    def _subtract_date(self,other):
        # other must be an instance of PolyDate
        other_universal = other.universal()
        return self._n - other_universal._n
    def __sub__(self,other):
        # other may be an int
        # or may be a PolyDate instance
        if type(other) == int:
            return self._subtract_int(other)
        if isinstance(other,PolyDate):
            return self._subtract_date(other)
        raise TypeError("UniversalDate.__sub__ can only be called with an integer or PolyDate instance")
    def __iadd__(self,num):
        if type(num) == int:
            return self._addition(num)
        raise TypeError("UniversalDate.__iadd__ can only be called with an integer")
    def __isub__(self,num):
        if type(num) == int:
            return self._subtract_int(num)
        raise TypeError("UniversalDate.__isub__ can only be called with an integer")
