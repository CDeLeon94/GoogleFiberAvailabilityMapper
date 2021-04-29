# TODO: Add support for apartments
import googlemaps as gmaps
import numpy
import requests

import concurrent.futures
import time
import os

API_Key = os.environ.get('GMaps_API_Key')

coord1 = (29.44578, -98.52163) 
coord2 = (29.45774, -98.54524)

latStart = min(coord1[0],coord2[0])
latEnd = max(coord1[0],coord2[0])
lonStart = min(coord1[1],coord2[1])
lonEnd = max(coord1[1],coord2[1])

#0.01 Low Res || 0.003 Med Res ||| 0.002 High Res
scanRes = 0.002

out = []
CONNECTIONS = 100
TIMEOUT = 5
urls = []

urlpre = "https://fiber.google.com/address?street_address="
urlmid = "&unit_number=&zip_code="
urlend = "&event_category=check%20address&event_action=submit&event_label=hero"
successurl = "https://fiber.google.com/signup/s/"

gmaps = gmaps.Client(key=API_Key)
fileNum=1
fileOutAvail = ""
fileOutAvail = ""
while not fileOutAvail:
    try:
        fileOutAvail  = open("dataAvail"+str(fileNum)+".csv", "x")
    except Exception as e:
        fileNum += 1

try:
    fileOutAvailMain  = open("dataAvail.csv", "a")
except Exception as e:
    print("dataAvail.csv is not available for writing. \nTERMINATING")
    exit()

fileOutAvail.write("Availability,StreetAddress,Zipcode\n")

latChecks = (latEnd - latStart) / scanRes
lonChecks = (lonEnd - lonStart) / scanRes
numChecks = int(lonChecks * latChecks);

cont = input(f"Starting {numChecks} checks. \nContinue? [Y/N]: ")
if 'y' not in cont.lower():
    exit()

currcheck = 0
coordsList = []
availList = []

def get_addr(coords):
    addr = gmaps.reverse_geocode(coords)
    return addr

def hasFiber(addr):
    address = ''
    zipcode = ''
    streetNum = ''
    route = ''
    for addComp in addr[0]['address_components']:
        if 'street_number' in addComp['types']:
            streetNum = addComp['long_name']
        if 'route' in addComp['types']:
            route = addComp['long_name']
        if 'postal_code' in addComp['types']:
            zipcode = addComp['long_name']
    address = streetNum + " " + route
    fullurl = urlpre + address.replace(" ","%20") + urlmid + zipcode + urlend

    r = requests.head(fullurl, allow_redirects=True)
    if successurl in r.url:
        return "AVAILABLE," + str(address) + ","+ str(zipcode)+"\n"
    else:
        return ""

for lat in numpy.arange(latStart, latEnd, scanRes): 
    for lon in numpy.arange(lonStart, lonEnd, scanRes):
        coordsList.append((lat,lon))

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(get_addr, coords) for coords in coordsList)
    time1 = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)

            print(str(len(out)),end="\r")

    time2 = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(hasFiber, addr) for addr in out)
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            if data:
                fileOutAvail.write(data)
                fileOutAvailMain.write(data)

            print(str(len(out)),end="\r")

fileOutAvail.close()
fileOutAvailMain.close()
