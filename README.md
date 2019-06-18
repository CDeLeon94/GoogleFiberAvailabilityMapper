# GoogleFiberAvailabilityScanner

Scrapes the google fiber website to check if a series of points within a region have Google Fiber available.
Results are written out in 2 CSV files, one cumulative file and one for each individual scan.  

# Requirements
 - Python 3
 - Google Maps API Access
 
# WARNING
This script can utilize a very high number of API requests in a very fast manner.  
Scan small areas with an appropriate resolusion, or set limits on your Google Maps API Dashboard. 
