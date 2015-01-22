import sys
import ptvsd
import signal
import SmartDoor
import SmartDoorConfig
import RPi.GPIO as GPIO

ptvsd.enable_attach(None)
should_read_sensor = True


def read_sensor():
    """ Reads the specified GPIO pins via the config
        file and processes them via the SmartDoor script.
    """

    config = SmartDoorConfig.read_config()
    led_pin = int(config['gpio_pin_led'])
    sensor_pin = int(config['gpio_pin_sensor'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)                                # LED
    GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Sensor

    try:
        print("{0} started and waiting for sensor input".format(__file__))
        while should_read_sensor:
            button_pressed = GPIO.input(sensor_pin)
            if button_pressed:
                GPIO.output(led_pin, True)
                SmartDoor.take_photo_and_push(config['pushbullet_auth_key'], config['pushbullet_device_names'])
                while button_pressed:
                    button_pressed = GPIO.input(sensor_pin)
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