#!/bin/python3.8
import csv
import os
import xml.etree.ElementTree as ET


# Standard amount by which bandwidth should be raised or lowered (Kbps)
incrementAmount = 1000
decrementAmount = 1000

# Max bandwidth (in Kbps)
maxNetworkBandwidth = 25000 * 30

configFile = 'config.xml'       # pfSense XML setting file (FIXME: Restore this path to '/conf/config.xml')
classifyFile = 'classData.csv'  # classify script output file


def readClassifyData():

    # Read data from classification script
    # Dictionary {Key: Value} where Key is <ip address> and Value is (Priority, )
    classifyData = {}

    with open(classifyFile) as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            classifyData[row[0]] = (row[1], row[2])

    return classifyData


def readXML():

    # Get current download bandwidth allocations from limiters

    tree = ET.parse(configFile)
    root = tree.getroot()

    currBW = {}

    for queue in root.findall('./dnshaper/queue'):
        ip_end = queue[0].text
        if len(ip_end) > 5:  # Catch limiters not named _# (where # is last octet of IP address)
            continue
        ip = "63.76.254.%s" % ip_end[1:]
        bw = queue[5][0][0].text

        currBW[ip] = bw

    return currBW


def genBWList(currentAllocation, classifyData):

    # Generate dictionary of IP : New Bandwidth Amount (In Kbps)

    newBWList = {}

    # TODO: This needs intelligence (where does bandwidth come from/go to)
    for key in currentAllocation:

        if key not in classifyData:
            continue

        if classifyData[key][1] == "up":
            newBWList[key] = str(int(currentAllocation[key]) + incrementAmount)
        elif classifyData[key][1] == "down":
            newBWList[key] = str(int(currentAllocation[key]) - decrementAmount)
        else:
            newBWList[key] = currentAllocation[key]

    return newBWList


def writeXML(newBW):

    # 1. Get new bandwidth amounts as input arg (dictionary)
    # 2. Parse /conf/config.xml and find each queue's IP
    # 3. Use IP as key in dictionary to get new bandwidth value
    # 4. Write out new XML file

    tree = ET.parse(configFile)
    root = tree.getroot()

    for queue in root.findall('./dnshaper/queue'):
        ip_end = queue[0].text
        if len(ip_end) > 5:  # Catch limiters not named _# (where # is last octet of IP address)
            continue
        ip = "63.76.254.%s" % ip_end[1:]
        try:
            queue[5][0][0].text = newBW[ip]
        except KeyError:  # Skip queue if corresponding IP is not in dictionary
            continue

    tree.write(configFile)

    return 0


def reloadFirewall():

    # 1. Remove /tmp/config.cache (Reloads config file)
    # 2. Run /etc/rc.filter_configure (Reloads pfsense firewall)

    os.system('rm /tmp/config.cache')
    os.system('/etc/rc.filter_configure')

    return 0


def main():

    # 1. Get and store current bandwidth allocations
    # 2. Parse input data from Classify.py (CSV file)
    # 3. Generate list of new bandwidth allocations
    # 4. Write new allocation parameters out to XML File
    # 5. Reload firewall

    currAllots = readXML()
    classData = readClassifyData()
    newBW = genBWList(currAllots, classData)
    writeXML(newBW)
    # reloadFirewall()

    return 0


if __name__ == '__main__':
    main()
