#!/usr/local/bin/python3.8

import subprocess
from time import sleep


def flow():
    # Run iftop
    # Arguments: -t, text mode (remove ncurses)
    #            -c, configuration input file
    #
    # Redirct interface name and MAC address to /dev/null
    # grep to only keep lines with per-host data
    # Split each line into entry in list
    iftop = "iftop -t -c conf/.iftoprc -s 1 2>/dev/null | grep -A 1 -E '^   [0-9]'"
    proc_out = subprocess.run(args=iftop, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    top_list = proc_out.stdout.split("\n")

    # Remove blank lines from list
    while '' in top_list:
        top_list.remove('')

    # Count = 2 * number of hosts
    # Two lines per host (one up, one down)
    count = len(top_list)

    # Dictionary to hold host information, ingoing, and outgoing traffic
    global host_dict
    global host_list
    
    host_dict = {}
    host_list = []

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

        # Standardize units
        unit(up_rate)
        unit(down_rate)

        # Store data
        host_data = [up_rate, down_rate]
        host_dict[host_ip] = host_data
        host_list.append(host_ip)
        

def priority():
    # Classify each host's priority
    for ip in host_list:
        bandwidth = host_dict[ip]

        print(ip)
        print(bandwidth)

        # If Up < x && Down < u: Prio 0
        # If Up > x && Down < y: Prio 1
        # If Up < x && Down > y: Prio 2
        # If UP > x && Down > y: Prio 3


def unit(measure):
    return None



def main():
    flow()
    priority()

if __name__ == '__main__':
    main()

