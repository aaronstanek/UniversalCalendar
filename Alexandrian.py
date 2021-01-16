from .PolyDate import PolyDate
from .Universal import UniversalDate
from .DurationSum import DurationSum

month_lengths = DurationSum([
    30,30,30,30,30,30,
    30,30,30,30,30,30,
    5
])

month_lengths_leap = DurationSum([
    30,30,30,30,30,30,
    30,30,30,30,30,30,
    6
])

block_length = DurationSum([
    365, 365, 365, 366
])

day_names = [
    "Thursday", "Friday", "Saturday", "Sunday",
    "Monday", "Tuesday", "Wednesday"
]

class AlexandrianDate(PolyDate):
    # _n is the Alexandrian date number
    # this is universal - 103605
    # _year is the year in the Coptic Calendar
    # there is no year zero
    # _month is an int holding the month
    # it ranges 1 to 12
    # _day is an int holding the day number
    # it ranges 1 to 31
    # this calendar is proleptic,
    # leap days were not observed before ~20 BC
    # and the Julian Calendar on which this calendar is based
    # observed leap days inconsistently before 8 AD
    def __init__(self,*args,**kwargs):
        # args may have one of three forms
        # [int] -> the value of _n
        # [int,int,int] -> the year, month, day (checked for correctness)
        # [PolyDate] -> a PolyDate to build from
        if len(args) == 1:
            if type(args[0]) == int:
                # Alexandrian Date number
                self._n = args[0]
                self._set_ymd()
                return
            if isinstance(args[0],PolyDate):
                self._n = args[0].universal()._n - 103605
                self._set_ymd()
                return
            raise ValueError("AlexandrianDate can only be constructed from integers or PolyDate instances")
        elif len(args) == 3:
            for i in range(3):
                if type(args[i]) != int:
                    raise TypeError("AlexandrianDate constructor was expecting [integer,integer,integer]")
            args = list(args)
            if "numbering" in kwargs:
                numbering = kwargs["numbering"]
                if type(numbering) != str:
                    raise TypeError("AlexandrianDate numbering must be a string")
                if numbering == "coptic":
                    pass
                elif numbering == "ethiopian":
                    args[0] = AlexandrianDate._convert_ethiopian(args[0])
                else:
                    raise ValueError("Invalid numbering")
            else:
                raise ValueError("AlexandrianDate constructor requires that a numbering be specified")
            AlexandrianDate.validate(*args)
            self._year = args[0]
            self._month = args[1]
            self._day = args[2]
            self._set_n()
            return
        raise ValueError("AlexandrianDate constructor was expecting either 1 or 3 arguments")
    lower_bound = None
    upper_bound = None
    def universal(self):
        return UniversalDate(self._n + 103605)
    def number(self):
        return self._n
    def __str__(self):
        return "AlexandrianDate(" + str(self._year) + "/" + str(self.year_ethiopian()) + "," + str(self._month) + "," + str(self._day) + ")"
    def _addition(self,num):
        # num must be an integer
        return AlexandrianDate(self._n + num)
    def _subtract_int(self,num):
        # num must be an integer
        return AlexandrianDate(self._n - num)
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
        return year % 4 == 3
    @staticmethod
    def validate(year,month,day):
        if year == 0:
            raise ValueError("The Coptic Calendar does not have a year 0, use -1 instead")
        if month < 1 or month > 13:
            raise ValueError("AlexandrianDate month must be between 1 and 13")
        leap = AlexandrianDate.is_leap_year(year)
        if leap:
            days_in_month = month_lengths_leap.get(month-1)
        else:
            days_in_month = month_lengths.get(month-1)
        if day > days_in_month or day < 1:
            raise ValueError("AlexandrianDate day must be between 1 and the maximum number of days in the month")
        # it is validated
    def _set_n(self):
        leap = AlexandrianDate.is_leap_year(self._year)
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
        leap = year_in_block == 3
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
    def year_coptic(self):
        return self._year
    def coptic(self):
        return "CopticDate(" + str(self._year) + "," + str(self._month) + "," + str(self._day) + ")"
    def year_ethiopian(self):
        y = self._year
        if y <= -1:
            y += 1
        y += 276
        if y <= 0:
            y -= 1
        return y
    def ethiopian(self):
        return "EthiopianDate(" + str(self.year_ethiopian()) + "," + str(self._month) + "," + str(self._day) + ")"
    @staticmethod
    def _convert_ethiopian(year):
        if year == 0:
            raise ValueError("The Ethiopian Calendar does not have a year 0, use -1 instead")
        if year <= -1:
            year += 1
        year -= 276
        if year <= 0:
            year -= 1
        return year