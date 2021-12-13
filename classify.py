#!/usr/local/bin/python3.8

import re
import subprocess
from time import sleep


# Get bandwidth data from iftop and parse
def flow():
    # Run iftop
    # Arguments: -t, text mode (remove ncurses)
    #            -c, configuration input file
    #            -s #, measure for # seconds
    #
    # Redirect stderr to /dev/null
    # Take stdout output and split each line into list
    iftop = "iftop -t -c .iftoprc -s 3"
    proc_out = subprocess.run(args=iftop, shell=True, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    top_list = proc_out.stdout.split("\n")

    # Trim list to only contain relevant lines of data (data with per IP bandwidth)
    data_list = []

    for i in range(len(top_list)):
        if re.search('^   [0-9]', top_list[i]):
            data_list.append(top_list[i])
            data_list.append(top_list[i+1])
            i+1

    # Count = 2 * number of hosts
    # Two lines per host (one upload, one download)
    count = len(data_list)
    
    # If list is empty, no data to work on
    if count < 2:
        return -1


    # Dictionary to hold host information, in-coming, and out-going traffic
    global host_dict
    global host_list

    host_dict = {}
    host_list = []

    #
    # For each host upload/download pair, extract information into format below
    #
    #     Host     |  Up Rate | Down Rate
    #   <ip_addr>  |   Mbps   |  Mbps
    #   <ip_addr>  |   Mbps   |  Mbps
    #      ""      |    ""    |   ""
    for i in range(int(count/2)):
        down_list = data_list[i*2].split(" ")
        up_list = data_list[(i*2)-1].split(" ")

        while '' in up_list:
            up_list.remove('')

        while '' in down_list:
            down_list.remove('')
        
        host_ip = up_list[0]
        up_rate = up_list[2]
        down_rate = down_list[3]

        # Standardize units
        up_rate = unit(up_rate)
        down_rate = unit(down_rate)

        # Store data
        host_data = [up_rate, down_rate]
        host_dict[host_ip] = host_data
        host_list.append(host_ip)


# Classify each host's priority
def priority():
    for ip in host_list:
        bandwidth = host_dict[ip]

        print (ip)
        print(bandwidth)

        # If Up < x && Down < y: Prio 0
        # If Up > x && Down < y: Prio 1
        # If Up < x && Down > y: Prio 2
        # If Up > x && Down > y: Prio 3
        # TODO: Consider special file I/O priorities (since they can use as much as possible)


# Strip unit, standardize to Kbps
def unit(measure):
    if "Mb" in measure:
        ret = float(measure.strip("Mb")) * 1024
        return ret
    elif "Kb" in measure:
        ret = float(measure.strip("Kb"))
        return ret
    elif "b" in measure:
        ret = float(measure.strip("b"))
        return ret


def main():
    if flow() != -1:
        priority()
    else:
        print("No data found")


if __name__ == '__main__':
    main()

