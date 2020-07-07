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

quart_length = DurationSum([
    366, 365, 365, 365
])

quart_length_short = DurationSum([
    365, 365, 365, 365
])

century_length = DurationSum([
    36525, 36524, 36524, 36524
])

day_names = [
    "Saturday", "Sunday", "Monday", "Tuesday",
    "Wednesday", "Thursday", "Friday"
]

class GregorianDate(PolyDate):
    # _n is the Gregorian date number
    # it also happens to be the universal date number
    # _year is the standard Gregorian year number
    # there is no year zero
    # _month is an int holding the month
    # it ranges 1 to 12
    # _day is an int holding the day number
    # it ranges 1 to 31
    def __init__(self,*args):
        # args may have one of three forms
        # [int] -> the value of _n
        # [int,int,int] -> the year, month, day (checked for correctness)
        # [PolyDate] -> a PolyDate to build from
        if len(args) == 1:
            if type(args[0]) == int:
                self._n = args[0]
                self._set_ymd()
                return
            if isinstance(args[0],PolyDate):
                self._n = args[0].universal()._n
                self._set_ymd()
                return
            raise ValueError("GregorianDate can only be constructed from integers or PolyDate instances")
        elif len(args) == 3:
            for i in range(3):
                if type(args[i]) != int:
                    raise TypeError("GregorianDate constructor was expecting [integer,integer,integer]")
            GregorianDate.validate(*args)
            self._year = args[0]
            self._month = args[1]
            self._day = args[2]
            self._set_n()
            return
        raise ValueError("GregorianDate constructor was expecting either 1 or 3 arguments")
    def universal(self):
        return UniversalDate(self._n)
    def number(self):
        return self._n
    def __str__(self):
        return "GregorianDate(" + str(self._year) + "," + str(self._month) + "," + str(self._day) + ")"
    def _addition(self,num):
        # num must be an integer
        return GregorianDate(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return GregorianDate(self._n - num)
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
        # year must be an integer
        # it is a standard gregorian year (there is no zero)
        # it may be negative
        # year -1 should behave like a century leap year
        if year <= -1:
            year += 1
        if year % 4 != 0:
            return False
        if year % 100 != 0:
            return True
        if year % 400 != 0:
            return False
        else:
            return True
    @staticmethod
    def validate(year,month,day):
        # year month and day all must be integers
        # year is ok no matter what
        if year == 0:
            raise ValueError("The Gregorian Calendar does not have a year 0, use -1 instead")
        leap = GregorianDate.is_leap_year(year)
        if month > 12 or month < 1:
            raise ValueError("GregorianDate month must be between 1 and 12")
        if leap:
            days_in_month = month_lengths_leap.get(month-1)
        else:
            days_in_month = month_lengths.get(month-1)
        if day > days_in_month or day < 1:
            raise ValueError("GregorianDate day must be between 1 and the maximum number of days in the month")
        # it is validated
    def _set_n(self):
        leap = GregorianDate.is_leap_year(self._year)
        # each block is 400 years
        y = self._year
        if y < 1:
            y += 1
        year_in_block = y % 400
        year_block = (y - year_in_block) // 400
        total = 146097 * year_block
        # total has the number of days from the epoch
        # to the start of the block
        year_in_century = year_in_block % 100
        century = year_in_block // 100
        if century != 0:
            total += century_length.forward(century)
        # total has the number of days from the epoch
        # to the start of the century
        year_in_quart = year_in_century % 4
        quart = year_in_century // 4
        if quart != 0:
            total += 1461 * quart
            if century != 0:
                total -= 1
        # total has the number of days from the epoch
        # to the start of the quart
        if year_in_quart != 0:
            if century != 0 and quart == 0:
                total += quart_length_short.forward(year_in_quart)
            else:
                total += quart_length.forward(year_in_quart)
        # total now has the number of days from the epoch
        # to the start of the year
        if leap:
            total += month_lengths_leap.forward(self._month-1)
        else:
            total += month_lengths.forward(self._month-1)
        # total now has the number of days from the epoch
        # to the start of the month
        total += (self._day-1)
        # total is fully set
        self._n = total
    def _set_ymd(self):
        # each block is 400 years
        n_in_block = self._n % 146097
        year_block = (self._n - n_in_block) // 146097
        # find century
        century, n_in_century = century_length.backward(n_in_block)
        if century == 0:
            quart = n_in_century // 1461
            n_in_quart = n_in_century % 1461
        else:
            quart = (n_in_century + 1) // 1461
            if quart == 0:
                n_in_quart = n_in_century
            else:
                n_in_quart = (n_in_century + 1) % 1461
        # quart and n_in_quart are now set
        if century != 0 and quart == 0:
            year_in_quart, n_in_year = quart_length_short.backward(n_in_quart)
        else:
            year_in_quart, n_in_year = quart_length.backward(n_in_quart)
        # year_in_quart and n_in_year are now set
        if (century == 0 or quart != 0) and year_in_quart == 0:
            # it's a leap year
            month, n_in_month = month_lengths_leap.backward(n_in_year)
        else:
            # it's not a leap year
            month, n_in_month = month_lengths.backward(n_in_year)
        # we are done
        year = (year_block*400) + (century*100) + (quart*4) + year_in_quart
        if year < 1:
            year -= 1
        self._year = year
        self._month = month + 1
        self._day = n_in_month + 1
