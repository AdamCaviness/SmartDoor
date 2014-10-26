import RPi.GPIO as GPIO
import SmartDoor


def read_sensor():
    """ Reads the specified GPIO pins via the config
        file and processes them via the SmartDoor script.
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)    # Button
    GPIO.setup(16, GPIO.OUT)  # LED

    try:
        while True:
            button_unpressed = GPIO.input(7)
            if not button_unpressed:
                GPIO.output(16, True)
                SmartDoor.take_photo_and_push()
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