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
vessel1 = []
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

# Does this thing work?
print ('Hello World!')
# Cool, continue

# Read voyage data
with open('output/voyages.csv', 'r') as read_obj:
    csvTrackingReader = reader(read_obj)
    count = 0
    for row in csvTrackingReader:
        if count > 0:
            entry = {"vessel":row[0], "begin_port_id":row[3], "end_port_id":row[4]}
            data.append(dict(entry))
        count += 1


print "\n\n    VOYAGES:"
#for row in data:
    #print row

#freq = []
#for row in data:
#    if row['vessel'] == '170':
#        entry = [row['begin_port_id'], row['end_port_id']]
#        freq.append(entry)

#for row in freq:
#    print row

#frequencies = freq[::-1]
#print frequencies

#counts = collections.Counter()
#for sublist in frequencies:
#    counts.update(itertools.combinations(sublist, 2))

#common = counts.most_common()

#for row in common:
#    print row

#cur_port = frequencies[0][1]
#print "current port is ", cur_port

predictedVoyages = []
voyagesByVessel = []

for i in range (176):
    index = i+1
    entry = {'vessel': index, 'voyages': []}
    voyagesByVessel.append(dict(entry))

print voyagesByVessel

for v in range(176):
    vessel = v+1
    #print vessel
    freq = []
    for row in data:
        if int(row['vessel']) == vessel:
            #print vessel
            entry = [row['begin_port_id'], row['end_port_id']]
            voyagesByVessel[v]['voyages'].append(entry)

#for row in voyagesByVessel:
#    print row['vessel']
#    print row['voyages']

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

         
#for predict in predictedVoyages:
#    print "predict"
#    print predict
            
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
            
            #frequencies = freq[::-1]
            #print frequencies
            #counts = collections.Counter()
            #for sublist in frequencies:
            #    counts.update(itertools.combinations(sublist, 2))
            #common = counts.most_common()
            #cur_port = frequencies[0][1]
   
   
    #if int(row['vessel']) == ind:
    #    entry = [row['begin_port_id'], row['end_port_id']]
    #    freq.append(entry)
    #    frequencies = freq[::-1]
    #    #print frequencies
    #    counts = collections.Counter()
    #    for sublist in frequencies:
    #        counts.update(itertools.combinations(sublist, 2))
    #    common = counts.most_common()
    #    cur_port = frequencies[0][1]
    #    #print "current port is ", cur_port
    #    for i in range(3):
    #        flag = False
    #        for row in common:
    #            if flag == False:
    #                print row[0][0]
    #                if row[0][0] == cur_port:
    #                    print "predicted voyage ",i+1, " ", row[0]
    #                    entry = {'vessel':i+1, 'begin_port_id', 'end_port_id', 'voyage'}
    #                    cur_port = row[0][1]
    #                    print "new current port is ", cur_port
    #                    flag = True


    #for i in range(3):
    #    flag = False
    #    for row in common:
    #        if flag == False:
    #            print row[0][0]
    #            if row[0][0] == cur_port:
    #                print "predicted voyage ",i+1, " ", row[0]
    #                cur_port = row[0][1]
    #                print "new current port is ", cur_port
    #                flag = True

#print common[0][0][1]

# Write to "voyages.csv"
#with open('output/voyages.csv', 'w') as csvfile:
#    fieldnames = ['vessel', 'begin_date', 'end_date', 'begin_port_id', 'end_port_id']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#    writer.writeheader()
#    for row in voyages :
#        writer.writerow({
#            'vessel': row['vessel'],
#            'begin_date': row['begin_date'],
#            'end_date': row['end_date'],
#            'begin_port_id': row['begin_port_id'],
#            'end_port_id': row['end_port_id']
#        })

# El Fin