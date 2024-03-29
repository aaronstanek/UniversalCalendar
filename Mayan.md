# MayanDate

MayanDate encodes the Mayan Calendar

Its constructor arguments are the date in the long count calendar: b'ak'tun, k'atun, tun, winal, k'in

where each runs from 0 to 19, except winal
which runs from 0 to 17

Although dates after 19.19.19.17.19 are valid in the actual
Mayan Calendar, they are invalid in this implementation.

Traditionally, Gregorian dates 11 Aug 3114 BCE to 12 Nov 2720 BCE are represented
by Mayan dates 13.0.0.0.0 to 13.19.19.17.19. However, this leads to ambiguity
as Gregorian dates 21 Dec 2012 CE to 25 Mar 2407 CE are also represented
by the same Mayan date range. To avoid this ambiguity, in this implementation,
the former range is renumbered 0.0.0.0.0 to 0.19.19.17.19.

It also displays Tzolk'in and Haab' in standard notaiton.

It has the methods:
- long_count (display only the long count, as a string)
- tzolkin (display only Tzolk'in, as a string)
- haab (display only Haab', as a string)
- baktun (returns b'ak'tun number as int)
- katun (returns k'atun number as int)
- tun (returns tun number as int)
- winal (returns winal number as int)
- kin (returns k'in number as int)
- tzolkin_number (returns the number of the Tzolk'in date as int, 1 to 13)
- tzolkin_day (returns the name of the day as a string, first letter capitalized, appostrophes where appropriate)
- haab_number (returns the number of the day within the Haab' month, 0 to 19)
- haab_month (returns the name of the Haab' month, first letter capitalized, appostrophes where appropriate)

Correlation with Gregorian Calendar established by:
- https://en.wikipedia.org/wiki/Maya_calendar
- https://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar
- https://maya.nmai.si.edu/calendar/maya-calendar-converter