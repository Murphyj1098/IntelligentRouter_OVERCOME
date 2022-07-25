#!/bin/python3.8
from time import sleep
import subprocess

if __name__ == '__main__':

    for i in range(2):
        subprocess.Popen("./allocate.py")

        for j in range(6):
            subprocess.Popen("./classify.py")
            sleep(5)
