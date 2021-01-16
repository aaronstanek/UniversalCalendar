# AlexandrianDate

AlexandrianDate encodes the proleptic Coptic and Ethiopian Calendars

Its constructor arguments are year, month, day

Negative years correspond to time before beginning of the
respective era.
There is no year zero.

Month is the number of the month, 1 is Thout / Mäskäräm, 13 is Pi Kogi Enavot / Ṗagume.

Day is the day of the month, starting from 1 and ending with 5, 6, or 30.

It has the methods:
- year_coptic
- year_ethiopian
- month
- day

Correlation with Gregorian Calendar established by:
- https://www.calendar-converter.com/coptic/
- https://ethiopian-calendar.netlify.app/

Numberings
- coptic
- ethiopian