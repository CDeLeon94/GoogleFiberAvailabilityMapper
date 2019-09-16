# GoogleFiberAvailabilityScanner

Builds a map of available locations for Google Fiber in a given area. 

## View the map
Map is periodically updated on [Google My Maps](https://drive.google.com/open?id=1BmskoePJltElqjrGdvfk3NAz44toc1Fb&usp=sharing)

## How it's done
Utilizes Google’s reverse geocoding APIs and Python Requests package to scrape Google Fiber’s Availability website. The resulting data is exported to a csv that can be imported into your mapping application of choice. 


# Requirements
 - Python 3
 - Google Maps API Access
 
# WARNING
This script can utilize a very high number of API requests in a very fast manner.  
Scan small areas with an appropriate resolusion, or set limits on your Google Maps API Dashboard. 
