# MayanDate encodes the Mayan Calendar

Its constructor arguments are the date in the long count calendar: bʼakʼtun, k'atun, tun, winal, k'in

where each runs from 0 to 19, except winal
which runs from 0 to 17

Although dates after 19.19.19.17.19 are valid in the actual
Mayan Calendar, they are invalid in this implementation.

In the actual Mayan Calendar, dates 1.0.0.0.0 to 12.19.19.17.19
are ambiguous. They can refer to the present creation, or to the previous creation.
In this implementation, they refer only to the present creation.
(Gregorian 13 Nov 2720 BCE to 20 Dec 2012 CE)

In the actual Mayan Calendar, dates 13.0.0.0.0 to 13.19.19.17.19
are ambiguous. They can refer to either to the bʼakʼtun at the beginning of the
present creation, or to the bʼakʼtun starting 13 bʼakʼtuns after the start of the
present creation. To avoid this confusion, in this implementation, 13.0.0.0.0 to 13.19.19.17.19 refer to
the latter (starting Gregorian 21 Dec 2012 CE). The former (starting Gregorian 11 August 3114 BCE)
is renumbered 0.0.0.0.0 to 0.19.19.17.19

It also displays Tzolkʼin and Haab' in standard notaiton.

It has the methods:
- long_count (display only the long count, as a string)
- tzolkin (display only Tzolkʼin, as a string)
- haab (display only Haabʼ, as a string)
- baktun (returns bʼakʼtun number as int)
- katun (returns k'atun number as int)
- tun (returns tun number as int)
- winal (returns winal number as int)
- kin (returns k'in number as int)
- tzolkin_number (returns the number of the Tzolkʼin date as int, 1 to 13)
- tzolkin_day (returns the name of the day as a string, first letter capitalized, appostrophes where appropriate)
- haab_number (returns the number of the day within the Haabʼ month, 0 to 19)
- haab_month (returns the name of the Haabʼ month, first letter capitalized, appostrophes where appropriate)
