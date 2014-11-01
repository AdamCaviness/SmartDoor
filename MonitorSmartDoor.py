import sys
import subprocess


def get_processes():
    p = subprocess.Popen(['pgrep', '-f', '-l', 'SmartDoorHost'], stdout=subprocess.PIPE)
    output, err = p.communicate()
    return output


def is_running(print_result):
    process_count = 0
    processes = get_processes()

    for line in processes.splitlines():
        process_count += 1

    if process_count > 0:
        if print_result:
            print('SmartDoor is running')
        return True
    else:
        if print_result:
            print('SmartDoor is not running')
        return False

    sys.exit()

if __name__ == '__main__':
    # Being executed as a script
    is_running(True)
