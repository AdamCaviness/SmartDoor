import os
import sys
import signal
import MonitorSmartDoor


def kill():
    """ Gracefully stops all SmartDoor processes.
    """
    process_count = 0

    if MonitorSmartDoor.is_running(False):
        processes = MonitorSmartDoor.get_processes()

        for line in processes.splitlines():
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

if __name__ == '__main__':
    # Being executed as a script
    kill()