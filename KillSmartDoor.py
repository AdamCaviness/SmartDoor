import os
import sys
import signal
import subprocess

process_count = 0
p = subprocess.Popen(['pgrep', '-f', 'SmartDoorHost'], stdout=subprocess.PIPE)
output, err = p.communicate()

for line in output.splitlines():
    process_count += 1
    line = bytes.decode(line)
    print("Killing SmartDoor process: {0}".format(line))
    pid = int(line.split(None, 1)[0])
    os.kill(pid, signal.SIGTERM)

if process_count > 0:
    print("{0} SmartDoor processes killed".format(process_count))
else:
    print('There were no SmartDoor processes running')

sys.exit()