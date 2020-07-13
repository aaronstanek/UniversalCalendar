from .PolyDate import PolyDate
from .Universal import UniversalDate
from .DurationSum import DurationSum

month_lengths = [
    30, 29, 30, 29,
    30, 29, 30, 29,
    30, 29, 30, 29
]

month_lengths_leap = [
    30, 29, 30, 29,
    30, 29, 30, 29,
    30, 29, 30, 30
]

# leap years are those mod 30
# 2, 5, 7, 10, 13, 15, 18, 21, 24, 26, 29

year_length = [
    354, 354, 355, 354, 354,
    355, 354, 355, 354, 354,
    355, 354, 354, 355, 354,
    355, 354, 354, 355, 354,
    354, 355, 354, 354, 355,
    354, 355, 354, 354, 355
    ]

class IslamicDate(PolyDate):
    # _n is the IslamicDate number
    # _year is years in the Islamic Calendar
    # there is no year zero
    # _month is the month (1 to 12)
    # _day is the day (1 to 30)
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
            raise ValueError("IslamicDate can only be constructed from integers or PolyDate instances")
        elif len(args) == 3:
            for i in range(3):
                if type(args[i]) != int:
                    raise TypeError("IslamicDate constructor was expecting [integer,integer,integer]")
            IslamicDate.validate(*args)
            self._year = args[0]
            self._month = args[1]
            self._day = args[2]
            self._set_n()
            return
        raise ValueError("IslamicDate constructor was expecting either 1 or 3 arguments")
    lower_bound = None
    upper_bound = None
    leap_years = [2, 5, 7, 10, 13, 15, 18, 21, 24, 26, 29]
    @staticmethod
    def is_leap_year(year):
        # year must be an integer
        # it cannot be zero
        if year <= -1:
            year += 1
        return (year % 30) in IslamicDate.leap_years
    @staticmethod
    def validate(year,month,day):
        # year month and day all must be integers
        # year is ok no matter what
        if year == 0:
            raise ValueError("The Islamic Calendar does not have a year 0, use -1 instead")
        leap = IslamicDate.is_leap_year(year)
        if month > 12 or month < 1:
            raise ValueError("IslamicDate month must be between 1 and 12")
        if leap:
            days_in_month = month_lengths_leap.get(month-1)
        else:
            days_in_month = month_lengths.get(month-1)
        if day > days_in_month or day < 1:
            raise ValueError("IslamicDate day must be between 1 and the maximum number of days in the month")
        # it is validated
    def _set_n(self):
        leap = IslamicDate.is_leap_year(self._year)
        # each block is 30 years, 10631 days
        y = self._year
        if y <= -1:
            y += 1
        year_in_block = y % 30
        year_block = (y - year_block) // 30
        # start setting the total
        total = year_block * 10631
        total += year_length.forward(year_in_block)
        # total has the number of days from the epoch
        # to the start of the year
        if leap:
            total += month_lengths_leap.forward(self._month-1)
        else:
            total += month_lengths.forward(self._month-1)
        # total has the number of days from the epoch
        # to the start of the month
        total += (self._day - 1)
        # total is set
        self._n = total
    def _set_ymd(self):
        # each block is 30 years, 10631 days
        n_in_block = self._n % 10631
        year_block = (self._n - n_in_block) // 10631
        year_in_block, n_in_year = year_length.backward(n_in_block)
        leap = year_in_block in IslamicDate.leap_years
        if leap:
            month, n_in_month = month_lengths_leap.backward(n_in_year)
        else:
            month, n_in_month = month_lengths.backward(n_in_year)
        year = (year_block*30) + year_in_block
        if year <= 0:
            year -= 1
        self._year = year
        self._month = month + 1
        self._day = n_in_month + 1