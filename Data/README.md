# Data Directory

This directory contains the raw data for the initial test of the developed algorithm as well as basic visualizations of this data.

<br>

## Directory Layout

RawData/ contains CSV files for each household included in the test. The format of the data is as follows:
```
Timestamp 1 (Unix time), Measured Download (Kbps)
Timestamp 2 (Unix time), Measured Download (Kbps)
Timestamp 3 (Unix time), Measured Download (Kbps)
...
```

UsageGraphs/ contains one PNG file for each house included in the test. These graphs show the usage between 08/01/22 - 08/15/22