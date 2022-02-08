#!/usr/local/bin/python3.8

import os
import xml.etree.ElementTree as ET

def main():
    
    # 1. Get classification data from classify.py
    # 2. Determine how much bandwidth each host is limited to
    # 3. Parse /conf/config.xml and set host's limiters to new limit
    # 4. Remove /tmp/config.cache (Reloads config file)
    # 5. Run /etc/rc.filter_configure (Reloads pfsense firewall)

    tree = ET.parse('/conf/config.xml')
    root = tree.getroot()

    for queue in root.findall('./dnshaper/queue'):
        queue[5][0][0].text = '100'

    tree.write('/conf/config.xml')

    os.system('rm /tmp/config.cache')
    os.system('/etc/rc.filter_configure')


if __name__ == '__main__':
    main()
