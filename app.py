# imports
import csv
from csv import reader
import datetime
from datetime import timedelta, date, datetime
from config import *
import collections
import itertools

# init
data = []
ports = []
prevSpeed=0
curSpeed=0
curLat = ''
preLat = ''
curLong = ''
prevLong = ''
inTransit = False
lastPort = []
voyages = []
departingLat = ''
departingLong = ''
arrivalLat = ''
arrivalLong = ''
departingDate = ''
arrivalDate = ''
tracking = []
sortedTracking = []
predictedVoyages = []
voyagesByVessel = []

# Does this thing work?
print ('Hello World!')
# Cool, continue

def getPort(la, lo):
    flag = 0
    print "get port for: (",la,",",lo,")"

    if len(la) < 1 or len(lo) < 0:
        print "empty lat, long"
        return 0
    for p in ports:
        pLa = p['lat']
        pLo = p['long']

        if "." in pLa:
            pLat = pLa[:pLa.index(".") + 2]
        else:
            pLat = pLa

        if "." in pLo:
            pLong = pLo[:pLo.index(".") + 2]
        else:
            pLong = pLo

        if float(pLat) > (float(la)-0.5) and float(pLat) < (float(la)+0.5) and float(pLong) > (float(lo)-0.5) and float(pLong) < (float(lo)+0.5):
            print "found port - ", p['port']
            flag = 1
            return p['port']
    if flag < 1:
        return 0
        print "failed to identify port"
    return

# Read vessel tracking data
with open('data/tracking.csv', 'r') as read_obj:
    csvTrackingReader = reader(read_obj)
    count = 0
    for row in csvTrackingReader:
        if count > 0:
            entry = {"vessel":row[0], "datetime":row[1], "lat":row[2], "long":row[3], "heading":row[4], "speed": row[5], "draft": row[6]}
            data.append(dict(entry))
        count += 1

# Read port data
with open('data/ports.csv', 'r') as read_obj:
    csvPortReader = reader(read_obj)
    count = 0
    for row in csvPortReader:
        if count > 0:
            entry = {"port":row[0], "lat":row[1], "long":row[2]}
            ports.append(dict(entry))
        count += 1

for i in range(176):
    index = i+1
    entry = {"vessel":index, "data": []}
    tracking.append(dict(entry))
    sortedTracking.append(dict(entry))

for i in range(176):
    index = i+1
    for row in data:
        if int(row['vessel']) == index:
            tracking[i]["data"].append(row)

# sort the array
for i in range(len(tracking)):
    sortedTracking[i]["data"] = sorted(tracking[i]["data"], key=lambda t: datetime.strptime(t['datetime'], '%Y-%m-%d %H:%M:%S'))

count = 0
for i in range(len(sortedTracking)):
    curSpeed = 0
    prevSpeed = 0
    prevLat = ''
    prevLong = ''
    curLat = ''
    curLong = ''
    date = ''
    count = 0
    inTransit = False
    for row in sortedTracking[i]['data']:
        #print row
        prevSpeed = curSpeed
        if len(row['speed']) > 0 and row['speed'] is not None and row['speed'] != 'NULL':
            curSpeed = float(row['speed'])
        else :
            curSpeed = prevSpeed
        prevLat = curLat
        prevLong = curLong
        curLat = row['lat']
        curLong = row['long']
        date = row['datetime']
        
        #if curSpeed == 0 and prevSpeed == 0:
            # ignore because vessel still hasnt moved
            #print "ignore - hasn't moved"
        #elif curSpeed != 0 and prevSpeed != 0:
            # ignore because vessel still moving
            #print "ignore - in transit"
        if count > 0 and curSpeed > 0 and prevSpeed == 0:
            # vessel has started moving
            #####print "started moving - departed port [",count,"] (",prevLat,",",prevLong,")"
            print "checking port (",prevLat,",",prevLong,")"
            checkPort = getPort(prevLat, prevLong)
            if checkPort > 0:
                inTransit = True
                departingPort = checkPort
                departingLat = prevLat
                departingLong = prevLong
                departingDate = date
                ####print "Valid departing port -- ", departingPort
            else:
                print "INVALID departing port"
            #print row
        elif count > 0 and curSpeed == 0 and inTransit == True:
            # vessel was moving and now at port
            #### print count, "Stopped --- checking if port exists ", row['datetime']
            print "checking port (",curLat,",",curLong,")"
            checkPort = getPort(curLat, curLong)
            ##### print checkPort
            if checkPort > 0:
                arrivalPort = checkPort
                arrivalLat = curLat
                arrivalLong = curLong
                arrivalDate = date
                #### print "    Port found: ", arrivalPort
                if arrivalPort == departingPort:
                    # arrival and departure the same - INVALID
                    #departingLat = curLat
                    #departingLong = curLong
                    #departingPort = arrivalPort
                    print "Same arrival and departure port --- invalid"
                else :
                    # arrival and departure different - VALID
                    #['vessel', 'begin_date', 'end_date', 'begin_port_id', 'end_port_id']
                    inTransit = False
                    #### print "ARRIVED at port [",count,"] (",curLat,",",curLong,")"
                    trip = {"vessel":row['vessel'], "begin_date": departingDate, "end_date": arrivalDate, "begin_port_id": departingPort, "end_port_id":arrivalPort }
                    voyages.append(dict(trip))
            else:
                print "    Port NOT FOUND keep going"
                
            #print row

        count += 1


# Write to "voyages.csv"
with open('output/voyages.csv', 'w') as csvfile:
    fieldnames = ['vessel', 'begin_date', 'end_date', 'begin_port_id', 'end_port_id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in voyages :
        writer.writerow({
            'vessel': row['vessel'],
            'begin_date': row['begin_date'],
            'end_date': row['end_date'],
            'begin_port_id': row['begin_port_id'],
            'end_port_id': row['end_port_id']
        })


for i in range (176):
    index = i+1
    entry = {'vessel': index, 'voyages': []}
    voyagesByVessel.append(dict(entry))

#print voyagesByVessel
#print data

for v in range(176):
    vessel = v+1
    #print vessel
    freq = []
    for row in voyages:
        if int(row['vessel']) == vessel:
            #print vessel
            entry = [row['begin_port_id'], row['end_port_id']]
            voyagesByVessel[v]['voyages'].append(entry)

for v in range(len(voyagesByVessel)):
    vessel = voyagesByVessel[v]['vessel']
    voyages = voyagesByVessel[v]['voyages']
    reverse = []
    if len(voyages) > 0:
        print vessel
        reverse = voyages[::-1] # reverse the list of voyages
        f = collections.Counter()
        for sublist in reverse:
            f.update(itertools.combinations(sublist, 2))
        frequencies = f.most_common()
        print frequencies
        currentPort = reverse[0][1]
        for i in range(3):
            flag = False
            count = 0
            end = len(frequencies)
            for row in frequencies:
                if flag == False:
                    #print row[0][0]
                    if row[0][0] == currentPort:
                        print "VESSEL: ",vessel,"    predicted voyage ",i+1, " ", row[0]
                        entry = {'vessel':vessel, 'begin_port_id': row[0][0], 'end_port_id': row[0][1], 'voyage': i+1}
                        predictedVoyages.append(dict(entry))
                        currentPort = row[0][1]
                        #print "new current port is ", currentPort
                        flag = True
                    else:
                        count += 1
                    if count == end:
                        # no known voyage frequency from the current port
                        print "uh oh we at the end for ", vessel
                        estimatedEndPort = frequencies[0][0][0]
                        #print estimatedEndPort
                        entry = {'vessel':vessel, 'begin_port_id': currentPort, 'end_port_id': estimatedEndPort, 'voyage': i+1}
                        predictedVoyages.append(dict(entry))
                        print "VESSEL: ",vessel,"    predicted voyage ",i+1, " ('",currentPort,"','",estimatedEndPort,"')" 
                        currentPort = estimatedEndPort

# Write to "predict.csv"
with open('output/predict.csv', 'w') as csvfile:
    fieldnames = ['vessel', 'begin_port_id', 'end_port_id', 'voyage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in predictedVoyages :
        writer.writerow({
            'vessel': row['vessel'],
            'begin_port_id': row['begin_port_id'],
            'end_port_id': row['end_port_id'],
            'voyage': row['voyage']
        })

# El Fin