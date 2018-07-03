#!/usr/bin/env python

import sys
import os
import json

# Import modules from the 'lib' subdirectory
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from kintyre_speedtest import main

def output_to_scriptedinput(event):
    json.dump(event, sys.stdout)
    sys.stdout.write("\n")

if __name__ == '__main__':
    main(output_to_scriptedinput)
