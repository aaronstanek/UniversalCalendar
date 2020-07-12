from .PolyDate import PolyDate
from .Universal import UniversalDate
from .DurationSum import DurationSum

month_lengths = DurationSum([
    31,28,31,30,31,30,
    31,31,30,31,30,31
])

month_lengths_leap = DurationSum([
    31,29,31,30,31,30,
    31,31,30,31,30,31
])

block_length = DurationSum([
    366, 365, 365, 365
])

day_names = [
    "Thursday", "Friday", "Saturday", "Sunday",
    "Monday", "Tuesday", "Wednesday"
]

class JulianDate(PolyDate):
    # _n is the Julian date number (not Julian day)
    # this is universal + 2
    # _year is the standard Julian year number CE/BCE
    # there is no year zero
    # _month is an int holding the month
    # it ranges 1 to 12
    # _day is an int holding the day number
    # it ranges 1 to 31
    # this calendar is proleptic, as falls out
    # of sync with the actual Julian Calendar on dates
    # before 8 AD
    def __init__(self,*args,**kwargs):
        # args may have one of three forms
        # [int] -> the value of _n
        # [int,int,int] -> the year, month, day (checked for correctness)
        # [PolyDate] -> a PolyDate to build from
        if len(args) == 1:
            if type(args[0]) == int:
                # Julian Date number
                self._n = args[0]
                self._set_ymd()
                return
            if isinstance(args[0],PolyDate):
                self._n = args[0].universal()._n + 2
                self._set_ymd()
                return
            raise ValueError("JulianDate can only be constructed from integers or PolyDate instances")
        elif len(args) == 3:
            for i in range(3):
                if type(args[i]) != int:
                    raise TypeError("JulianDate constructor was expecting [integer,integer,integer]")
            args = list(args)
            if "numbering" in kwargs:
                if kwargs["numbering"] == "berber":
                    args[0] = self._convert_berber(args[0])
                elif kwargs["numbering"] == "byzantine":
                    args[0] = self._convert_byzantine(args[0],args[1])
                elif kwargs["numbering"] == "march1":
                    args[0] = self._convert_march1(args[0],args[1])
                elif kwargs["numbering"] == "march25":
                    args[0] = self._convert_march25(*args)
                elif kwargs["numbering"] == "december25":
                    args[0] = self._convert_december25(*args)
                else:
                    raise ValueError("Invalid numbering")
            JulianDate.validate(*args)
            self._year = args[0]
            self._month = args[1]
            self._day = args[2]
            self._set_n()
            return
        raise ValueError("JulianDate constructor was expecting either 1 or 3 arguments")
    lower_bound = None
    upper_bound = None
    def universal(self):
        return UniversalDate(self._n - 2)
    def number(self):
        return self._n
    def __str__(self):
        return "JulianDate(" + str(self._year) + "," + str(self._month) + "," + str(self._day) + ")"
    def _addition(self,num):
        # num must be an integer
        return JulianDate(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return JulianDate(self._n - num)
    def year(self):
        return self._year
    def month(self):
        return self._month
    def day(self):
        return self._day
    def day_of_week(self):
        return day_names[self._n % 7]
    @staticmethod
    def is_leap_year(year):
        # year should be an integer
        # there is no zero
        if year <= -1:
            year += 1
        return year % 4 == 0
    @staticmethod
    def validate(year,month,day):
        if year == 0:
            raise ValueError("The Julian Calendar does not have a year 0, use -1 instead")
        leap = JulianDate.is_leap_year(year)
        if month < 1 or month > 12:
            raise ValueError("JulianDate month must be between 1 and 12")
        if leap:
            days_in_month = month_lengths_leap.get(month-1)
        else:
            days_in_month = month_lengths.get(month-1)
        if day > days_in_month or day < 1:
            raise ValueError("JulianDate day must be between 1 and the maximum number of days in the month")
        # it is validated
    def _set_n(self):
        leap = JulianDate.is_leap_year(self._year)
        # each block is 4 years (1461 days)
        y = self._year
        if y <= -1:
            y += 1
        year_in_block = y % 4
        year_block = (y - year_in_block) // 4
        total = year_block * 1461
        # total has the number of days from the epoch
        # to the start of the block
        total += block_length.forward(year_in_block)
        # total has the number of days from the epoch
        # to the start of the year
        if leap:
            total += month_lengths_leap.forward(self._month-1)
        else:
            total += month_lengths.forward(self._month-1)
        # total has the number of days from the epoch
        # to the start of the month
        total += self._day - 1
        # total is set
        self._n = total
    def _set_ymd(self):
        # each block is 4 years (1461 days)
        n_in_block = self._n % 1461
        year_block = (self._n - n_in_block) // 1461
        year_in_block, n_in_year = block_length.backward(n_in_block)
        leap = year_in_block == 0
        if leap:
            month_in_year, n_in_month = month_lengths_leap.backward(n_in_year)
        else:
            month_in_year, n_in_month = month_lengths.backward(n_in_year)
        year = (year_block*4) + year_in_block
        if year < 1:
            year -= 1
        self._year = year
        self._month = month_in_year + 1
        self._day = n_in_month + 1
    # alternative numberings
    def year_berber(self):
        # Berber count is 950 years ahead of Anno Domini
        y = self._year
        if y <= -1:
            y += 1
        y += 950
        if y <= 0:
            y -= 1
        return y
    def berber(self):
        return "BerberDate(" + str(self.year_berber()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _convert_berber(self,year):
        if year == 0:
            raise ValueError("The Berber Calendar does not have a year 0, use -1 instead")
        if year <= -1:
            year += 1
        year -= 950
        if year <= 0:
            year -= 1
        return year
    def year_byzantine(self):
        # Byzantine count is 5,508 years ahead of Anno Domini (Jan-Aug)
        # 5,508 years ahead (Sep-Dec)
        y = self._year
        if y <= -1:
            y += 1
        if self._month < 9:
            # (Jan-Aug)
            y += 5508
        else:
            # (Sep-Dec)
            y += 5509
        if y <= 0:
            y -= 1
        return y
    def byzantine(self):
        return "ByzantineDate(" + str(self.year_byzantine()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _convert_byzantine(self,year,month):
        if year == 0:
            raise ValueError("The Byzantine Calendar does not have a year 0, use -1 instead")
        if month < 1 or month > 12:
            raise ValueError("JulianDate month must be between 1 and 12")
        if year <= -1:
            year += 1
        if month < 9:
            # (Jan-Aug)
            year -= 5508
        else:
            # (Sep-Dec)
            year -= 5509
        if year <= 0:
            year -= 1
        return year
    def year_march1(self):
        # starting the year on March 1
        # year is the same (Mar-Dec)
        # year is one less (Jan-Mar)
        y = self._year
        if y <= -1:
            y += 1
        if self._month < 3:
            y -= 1
        if y <= 0:
            y -= 1
        return y
    def march1(self):
        return "JulianDate(Mar1)(" + str(self.year_march1()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _convert_march1(self,year,month):
        if year == 0:
            raise ValueError("The Julian Calendar does not have a year 0, use -1 instead")
        if year <= -1:
            year += 1
        if month < 3:
            year += 1
        if year <= 0:
            year -= 1
        return year
    def year_march25(self):
        # starting the year on March 25
        # year is the same (Mar25-Dec)
        # year is one less (Jan-Mar24)
        y = self._year
        if y <= -1:
            y += 1
        if self._month <= 2:
            y -= 1
        elif self._month == 3 and self._day <= 24:
            y -= 1
        if y <= 0:
            y -= 1
        return y
    def march25(self):
        return "JulianDate(Mar25)(" + str(self.year_march25()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _convert_march25(self,year,month,day):
        if year == 0:
            raise ValueError("The Julian Calendar does not have a year 0, use -1 instead")
        if year <= -1:
            year += 1
        if month <= 2:
            year += 1
        elif month == 3 and day <= 24:
            year += 1
        if year <= 0:
            year -= 1
        return year
    def year_december25(self):
        # starting the year on December 25
        # year is the same (Jan-Dec24)
        # year is one more (Dec25-Dec31)
        y = self._year
        if y <= -1:
            y += 1
        if self._month == 12 and self._day >= 25:
            y += 1
        if y <= 0:
            y -= 1
        return y
    def december25(self):
        return "JulianDate(Dec25)(" + str(self.year_december25()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _convert_december25(self,year,month,day):
        if year == 0:
            raise ValueError("The Julian Calendar does not have a year 0, use -1 instead")
        if month != 12:
            return year
        if day < 25:
            return year
        if year <= -1:
            year += 1
        year -= 1
        if year <= 0:
            year -= 1
        return year