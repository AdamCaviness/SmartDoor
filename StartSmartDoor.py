import sys
import subprocess
import SmartDoorConfig
import MonitorSmartDoor


def start(python_version):
    subprocess.Popen(['sudo', python_version, 'SmartDoorHost.py'])


def execute():
    config = SmartDoorConfig.read_config()
    if not MonitorSmartDoor.is_running(False):
        start(config['python_version'])
    else:
        print('SmartDoor is already running, consider running KillSmartDoor.py')

    sys.exit()

if __name__ == '__main__':
    # Being executed as a script
    execute()