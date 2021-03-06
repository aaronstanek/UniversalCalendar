# GregorianDate

GregorianDate encodes the proleptic Gregorian Calendar

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

Numberings
- default
- era_fascista (counts from 1922) (new year starts on 28 Oct)
- juche (counts from 1912)
- holocene (counts from 10001 BCE)
- minguo (counts from 1912)