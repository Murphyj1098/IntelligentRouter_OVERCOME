#!/usr/local/bin/python3.8

import os
from time import sleep

def flow():
    # Run iftop
    # Arguments: -t, text mode (remove ncurses)
    #            -c, configuration input file
    #
    # Redirct interface name and MAC address to /dev/null
    # grep to only keep lines with per-host data
    # Split each line into entry in list
    iftop = "iftop -t -c .iftoprc -s 1 2>/dev/null | grep -A 1 -E '^   [0-9]'"
    mes = os.popen(iftop).read()
    top_list = mes.split("\n")
    
    # Remove blank lines from list
    while '' in top_list:
        top_list.remove('')

    # Count = 2 * number of hosts
    # Two lines per host (one up, one down)
    count = len(top_list)

    # Dictionary to hold host information, ingoing, and outgoing traffic
    host_dict = {}
    
    #
    # For each host upload/download pair, extract information into below format
    #
    #     Host    |  Up Rate | Down Rate
    #   <ip addr> |   Mbps   |   Mbps
    #   <ip addr> |   Mbps   |   Mbps
    #      ""     |    ""    |    ""
    for i in range(int(count/2)):
        upload_list = top_list[i*2].split(" ")
        down_list = top_list[(i*2)-1].split(" ")

        while '' in upload_list:
            upload_list.remove('')

        while '' in down_list:
            down_list.remove('')

        
        host_ip = upload_list[1]
        up_rate = upload_list[3]
        down_rate = down_list[2]

        print("IP Address: " + host_ip)
        print("Upload (2 second average): " + up_rate + "ps")
        print("Download (2 second average): " + down_rate + "ps")

flow()

