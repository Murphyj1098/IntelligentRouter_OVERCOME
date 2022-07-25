#!/bin/python3.8
import time
import subprocess
import datetime
import logging

import classify

if __name__ == '__main__':

    date = datetime.date.today()
    logFileName = "./ClassifyLogs/{today}_classify.log".format(today=date)

    # Setup logging
    logging.basicConfig(filename=logFileName, filemode='a', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    nextStart = time.monotonic()
    delta = 6

    for i in range(2):
        subprocess.Popen("./allocate.py")

        for j in range(5):
            nextStart = nextStart + delta

            # Classify code here
            classify.main()

            # Wait until next classify time
            while nextStart > time.monotonic():
                time.sleep(0.1)
