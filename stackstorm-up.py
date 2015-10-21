#!/usr/bin/env python
import os
import sys
import subprocess

instance = sys.argv[1] if len(sys.argv) > 1 else "stackstorm-master"
user = sys.argv[2] if len(sys.argv) > 2 else "vagrant"

output = subprocess.check_output(
             ["ssh", "{}@{}".format(user, instance), "st2ctl", "status"])
statuses = output.split(os.linesep)

expected_similar = """st2actionrunner PID:
st2api PID:
st2auth PID:
st2sensorcontainer PID:
st2rulesengine PID:
st2web PID:
mistral PID:
st2resultstracker PID:
st2notifier PID:"""

patterns = expected_similar.split(os.linesep)

errors = False

for pattern in patterns:
    match = any([status.startswith(pattern) for status in statuses])
    print "Match:", pattern, match
    if not match:
        errors = True

if errors:
    print "Some errors from st2ctl status"
    sys.exit(1)

