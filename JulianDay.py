from .PolyDate import PolyDate
from .Universal import UniversalDate

class JulianDay(PolyDate):
    # _n is the julian date number
    # _n = 0 -> universal date = -1721060
    def __init__(self,other):
        if type(other) == int:
            self._n = other
            return
        if isinstance(other,PolyDate):
            other_universal = other.universal()
            self._n = other_universal._n + 1721060
            return
        raise TypeError("JulianDay can only be constructed from an integer or PolyDate instance")
    lower_bound = None
    upper_bound = None
    def universal(self):
        return UniversalDate(self._n - 1721060)
    def number(self):
        return self._n
    def __str__(self):
        return "JulianDay(" + str(self._n) + ")"
    def _addition(self,num):
        # num must be an integer
        return JulianDay(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return JulianDay(self._n - num)