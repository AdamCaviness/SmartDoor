import os
import sys
import json
import SmartDoor
import RPi.GPIO as GPIO


def read_sensor():
    """ Reads the specified GPIO pins via the config
        file and processes them via the SmartDoor script.
    """
    executing_path = os.path.dirname(sys.argv[0])
    config_filename = os.path.join(executing_path, 'config.json')
    with open(config_filename) as conf:
        config = json.load(conf)

    led_pin = int(config['gpio_pin_led'])
    sensor_pin = int(config['gpio_pin_sensor'])
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led_pin, GPIO.OUT)    # LED
    GPIO.setup(sensor_pin, GPIO.IN)  # Sensor

    try:
        while True:
            button_unpressed = GPIO.input(7)
            if not button_unpressed:
                GPIO.output(16, True)
                SmartDoor.take_photo_and_push(config['pushbullet_auth_key'], config['pushbullet_device_names'])
                while not button_unpressed:
                    button_unpressed = GPIO.input(7)
                GPIO.output(16, False)
    except KeyboardInterrupt:
        print('SmartDoor exited gracefully')
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    # Being executed as a script
    read_sensor()