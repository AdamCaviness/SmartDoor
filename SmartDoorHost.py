import sys
import signal
import SmartDoor
import SmartDoorConfig
import RPi.GPIO as GPIO

should_read_sensor = True


def read_sensor():
    """ Reads the specified GPIO pins via the config
        file and processes them via the SmartDoor script.
    """

    config = SmartDoorConfig.read_config()
    led_pin = int(config['gpio_pin_led'])
    sensor_pin = int(config['gpio_pin_sensor'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)    # LED
    GPIO.setup(sensor_pin, GPIO.IN)  # Sensor

    try:
        print("{0} started and waiting for sensor input".format(__file__))
        while should_read_sensor:
            button_unpressed = GPIO.input(sensor_pin)
            if not button_unpressed:
                GPIO.output(led_pin, True)
                SmartDoor.take_photo_and_push(config['pushbullet_auth_key'], config['pushbullet_device_names'])
                while not button_unpressed:
                    button_unpressed = GPIO.input(sensor_pin)
                GPIO.output(led_pin, False)
    finally:
        GPIO.cleanup()
        sys.exit()


def handler(signum=None, frame=None):
    print("{0} exiting gracefully".format(__file__))
    global should_read_sensor
    should_read_sensor = False

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, handler)

if __name__ == '__main__':
    # Being executed as a script
    read_sensor()