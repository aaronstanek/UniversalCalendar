# JulianDay

JulianDay encodes the Julian Day

Its constructor argument is the Julian Day number

Because Julian Days begin and end at noon UTC it is hard to establish
an exact correlation between it and most other calendar systems (which typically start a day at midnight, dusk, or dawn)

This implementation attaches the Julian Day to the GregorianDate which began 12 hours before it (UTC)

So, Gregorian 21 Dec 2012 CE corresponds to Julian Day 2,456,283

Correlation with Gregorian Calendar established by:
- https://en.wikipedia.org/wiki/Julian_day
- https://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar