import os
import re
import sys
import json
import picamera
import datetime
from pushbullet import PushBullet


def take_photo_and_push():
    """ Takes a photo and sends to the cloud.
        Implements pushbullet.py, see https://pypi.python.org/pypi/pushbullet.py
        Implements picamera.py, see http://raspberrypi.org/picamera-pure-python-interface-for-camera-module
    """
    executing_path = os.path.dirname(sys.argv[0])
    config_filename = os.path.join(executing_path, 'config.json')
        
    with open(config_filename) as conf:
        config = json.load(conf)

    file_name = datetime.datetime.now().strftime("%I:%M%p %m-%d-%Y") + '.jpg'
    file_path = os.path.join('/home/pi', file_name)
    with picamera.PiCamera() as camera:
        camera.vflip = True
        camera.hflip = True
        camera.resolution = (1024, 768)
        camera.capture(file_path)

    pb = PushBullet(config['auth_key'])

    with open(file_path, 'rb') as pic:
        message = 'SmartDoor ' + re.sub('.png', "", file_name)
        success, file_data = pb.upload_file(pic, message, 'image/jpeg',)

    upload_message = "{0} uploading picture {1} to url {2}".format(
        'Success' if str(success) else 'Failure',
        file_data.get('file_name'),
        file_data.get('file_url'))
    print(upload_message)
    devices = pb.devices

    for deviceName in config['device_names']:
        device_list = [d for d in devices if d.nickname == deviceName and d.active]
        device = device_list[0] if device_list else None
        if device is not None:
            success, push = device.push_file(**file_data)
            print('Successfully pushed ' + push.get('iden') + ' to ' + device.nickname)

    os.remove(file_path)

if __name__ == '__main__':
    # Being executed as a script
    take_photo_and_push()
