# IslamicDate

IslamicDate implements a tabluar Islamic Calendar.

The actual Islamic Calendar relies on human observations of the moon.
This implementation uses Microsoft's Kuwaiti algorithm to approximate
the date in the Islamic Calendar system. For modern uses, this approximation
should be accurate to within one day. For dates before 10 AH, it is uncertain
whether intercalation was used, potentially giving this approximation an
error of several months. (with a potential of several years' error for the distant past)

Its constructor arguments are year, month, day

Where AH corresponds to positive year numbers,
and BH corresponds to negative year numbers.
There is no year zero.

Month is the number of the month, 1 is al-Muḥarram, 12 is Dhu al-Hijjah.

Day is the day of the month, starting from 1 and ending with 29 or 30.

It has the methods:
- year
- month
- day
- day_of_week
- day_of_week_arabic

The first three return the internal state of the object.

The day_of_week returns a string with the common English name of the
day of the week.

The day_of_week_arabic returns a string with the common Arabic name of the
day of the week.

Correlation with Gregorian Calendar established by:
- http://joda-time.sourceforge.net/cal_islamic.html
- http://dictionnaire.sensagent.leparisien.fr/kuwaiti+algorithm/en-en/
- http://blog.androidrich.com/2012/12/famouse-algorithm-kuwaiti-algorithm-for.html