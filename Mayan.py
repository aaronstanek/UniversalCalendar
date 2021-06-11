from .PolyDate import PolyDate
from .Universal import UniversalDate

tzolkin_days = [
    "Imix", "Ik'", "Ak'b'al", "K'an", "Chikchan",
    "Kimi", "Manik'", "Lamat", "Muluk", "Ok",
    "Chuwen", "Eb'", "B'en", "Ix", "Men",
    "Kib'", "Kab'an", "Etz'nab'", "Kawak", "Ajaw"
]

haab_months = [
    "Pop", "Wo'", "Sip", "Sotz'", "Sek",
    "Xul", "Yaxk'in", "Mol", "Ch'en", "Yax",
    "Sak'", "Keh", "Mak", "K'ank'in", "Muwan",
    "Pax", "K'ayab'", "Kumk'u", "Wayeb'"
]

class MayanDate(PolyDate):
    # maintians long count,
    # Tzolk'in and Haab'
    # epoch aligns to the start of the long count
    # _n is universal + 1136777
    def __init__(self,*args):
        if len(args) == 1:
            if type(args[0]) == int:
                # MayanDate number
                self._n = args[0]
                self._set_counts()
                self._set_tzolkin()
                self._set_haab()
                return
            if isinstance(args[0],PolyDate):
                self._n = args[0].universal()._n + 1136777
                self._set_counts()
                self._set_tzolkin()
                self._set_haab()
                return
            raise ValueError("MayanDate can only be constructed from integers or PolyDate instances")
        elif len(args) == 5:
            # long count
            for i in range(5):
                if type(args[i]) != int:
                    raise TypeError("MayanDate constructor was expecting [integer,integer,integer,integer,integer]")
            MayanDate.validate_long_count(*args)
            self._baktun = args[0]
            self._katun = args[1]
            self._tun = args[2]
            self._winal = args[3]
            self._kin = args[4]
            self._set_n()
            self._set_tzolkin()
            self._set_haab()
            return
        raise ValueError("MayanDate constructor was expecting either 1 or 5 arguments")
    lower_bound = UniversalDate(-1136777)
    upper_bound = UniversalDate(1743222)
    def universal(self):
        return UniversalDate(self._n - 1136777)
    def number(self):
        return self._n
    def long_count(self):
        long = "LongCount(" + str(self._baktun) + "."
        long += str(self._katun) + "." + str(self._tun) + "."
        long += str(self._winal) + "." + str(self._kin) + ")"
        return long
    def tzolkin(self):
        tz = "Tzolk'in("
        tz += str(self._tzolkin_number) + " "
        tz +=  self._tzolkin_day + ")"
        return tz
    def haab(self):
        h = "Haab'("
        h += str(self._haab_number) + " "
        h += self._haab_month + ")"
        return h
    def __str__(self):
        total = "MayanDate(" + self.long_count()
        total += "," + self.haab()
        total += "," + self.tzolkin()
        total += ")"
        return total
    def _addition(self,num):
        # num must be an integer
        return MayanDate(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return MayanDate(self._n - num)
    def baktun(self):
        return self._baktun
    def katun(self):
        return self._katun
    def tun(self):
        return self._tun
    def winal(self):
        return self._winal
    def kin(self):
        return self._kin
    def tzolkin_number():
        return self._tzolkin_number
    def tzolkin_day():
        return self._tzolkin_day
    def haab_number():
        return self._haab_number
    def haab_month():
        return self._haab_month
    @staticmethod
    def validate_long_count(baktun,katun,tun,winal,kin):
        if baktun > 19:
            raise ValueError("MayanDate cannot encode dates after 19.19.19.17.19")
        if baktun < 0:
            raise ValueError("MayanDate cannot encode dates before 0.0.0.0.0")
        if katun > 19 or katun < 0:
            raise ValueError("MayanDate k'atun must be between 0 and 19")
        if tun > 19 or tun < 0:
            raise ValueError("MayanDate tun must be between 0 and 19")
        if winal > 17 or winal < 0:
            raise ValueError("MayanDate winal must be between 0 and 17")
        if kin > 19 or kin < 0:
            raise ValueError("MayanDate k'in must be between 0 and 19")
        # validated
    def _set_n(self):
        baktun = self._baktun
        katun = (baktun * 20) + self._katun
        tun = (katun * 20) + self._tun
        winal = (tun * 18) + self._winal
        kin = (winal * 20) + self._kin
        self._n = kin
    def _set_counts(self):
        n = self._n
        self._kin = n % 20
        n = n // 20
        self._winal = n % 18
        n = n // 18
        self._tun = n % 20
        n = n // 20
        self._katun = n % 20
        n = n // 20
        self._baktun = n
        MayanDate.validate_long_count(
            self._baktun, self._katun, self._tun,
            self._winal, self._kin
        )
    def _set_tzolkin(self):
        self._tzolkin_number = (self._n + 3) % 13 + 1
        self._tzolkin_day = tzolkin_days[(self._n + 19) % 20]
    def _set_haab(self):
        t = (self._n + 348) % 365
        self._haab_number = t % 20
        self._haab_month = haab_months[t // 20]