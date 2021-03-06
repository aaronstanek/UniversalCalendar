# JulianDate

JulianDate encodes the proleptic Julian Calendar

Its constructor arguments are year, month, day

Where CE/AD corresponds to positive year numbers,
and BCE/BC corresponds to negative year numbers.
There is no year zero.

Month is the number of the month, 1 is January, 12 is December.

Day is the day of the month, starting from 1 and ending with 28, 29, 30, or 31.

It has the methods:
- year
- month
- day
- day_of_week

The first three return the internal state of the object.

The last returns a string with the common English name of the
day of the week.

Correlation with Gregorian Calendar established by:
- https://en.wikipedia.org/wiki/Julian_calendar

Numberings
- default
- berber (counts from 950 BCE)
- byzantine (counts from 5509 BCE) (new year starts on 1 Sep)
- year starting on March 1 (march1)
- year starting on March 25 (march25)
- year starting on December 25 (december25)