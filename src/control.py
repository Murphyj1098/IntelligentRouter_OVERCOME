#!/usr/local/bin/python3.8
import time
import datetime
import logging

import classify
import allocate

if __name__ == '__main__':

    date = datetime.date.today()
    logFileName = "./Logs/{today}.log".format(today=date)

    # Setup logging
    logging.basicConfig(filename=logFileName, filemode='a', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    nextStart = time.monotonic()
    delta = 7.5  # 7.5 seconds between runs (time to perform all data collection and processing)

    for i in range(8):
        nextStart = nextStart + delta

        # Classify code here
        classData = classify.main()

        # Allocation code here
        allocate.main(classData)

        # Wait until next classify time
        if i != 7:
            while nextStart > time.monotonic():
                time.sleep(0.1)
