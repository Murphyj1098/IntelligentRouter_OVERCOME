#!/usr/local/bin/python3.8

import subprocess
from time import sleep

def main():
    
    # 1. Get classification data from classify.py
    # 2. Determine how much bandwidth each host is limited to
    # 3. Parse /conf/config.xml and set host's limiters to new limit
    # 4. Remove /tmp/config.cache (Reloads config file)
    # 5. Run /etc/rc.filter_configure (Reloads pfsense firewall)




if __name__ == '__main__':
    main()
