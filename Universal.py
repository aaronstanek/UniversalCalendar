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
    def number(self):
        return self._n
    def __str__(self):
        return "UniversalDate(" + str(self._n) + ")"
    def _addition(self,num):
        # num must be an integer
        return UniversalDate(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return UniversalDate(self._n - num)