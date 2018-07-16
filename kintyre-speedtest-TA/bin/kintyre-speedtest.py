#!/usr/bin/env python

import sys
import os
import re
import json

# Import modules from the 'lib' subdirectory
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from kintyre_speedtest import main, find_matching_interfaces


def get_splunk_uuid():
    splunk_home = os.environ.get("SPLUNK_HOME")
    if not splunk_home:
        # Fallback to relative (parent) path
        # ... /custom/splunk/etc/apps/kintyre-speedtest-TA/bin/kintyre-speedtest.py
        # XXX:  Test on windows.  Shouldn't matter when running from Splunk
        # XXX: Known issue if path contains symlinks (os.getcwd() resolves the path); could use $PWD
        splunk_home = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-5])
    instance_cfg = os.path.join(splunk_home, "etc", "instance.cfg")
    try:
        sys.stderr.write("Looking for instance data at {}\n".format(instance_cfg))
        data = open(instance_cfg, "r").read()
    except IOError:
        return
    me = re.search(r'guid\s*=\s*([A-Fa-f0-9-]+)', data)
    if me:
        return me.group(1).lower()

def output_to_scriptedinput(event):
    agent_info = event["agent"] = {}
    agent_info["_type"] = "splunk-scripted-input"
    uuid = get_splunk_uuid()
    if uuid:
        agent_info["uuid"] = uuid
    json.dump(event, sys.stdout)
    sys.stdout.write("\n")


if __name__ == '__main__':
    interfaces = find_matching_interfaces("default")
    main(interfaces, output_to_scriptedinput)
