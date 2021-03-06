import os
import re
import picamera
import datetime
import SmartDoorConfig
from pushbullet import PushBullet


def take_photo_and_push(flip_pic_h, flip_pic_v, pushbullet_auth_key, pushbullet_device_names):
    """ Takes a photo and sends to the cloud via PushBullet.
        Implements pushbullet.py, see https://pypi.python.org/pypi/pushbullet.py
        Implements picamera.py, see http://raspberrypi.org/picamera-pure-python-interface-for-camera-module
    """
    file_name = datetime.datetime.now().strftime("%I:%M%p %m-%d-%Y") + '.jpg'
    file_path = os.path.join('/home/pi', file_name)
    with picamera.PiCamera() as camera:
        camera.hflip = flip_pic_h
        camera.vflip = flip_pic_v
        camera.resolution = (1024, 768)
        camera.capture(file_path)

    pb = PushBullet(pushbullet_auth_key)

    with open(file_path, 'rb') as pic:
        message = 'SmartDoor ' + re.sub('.png', "", file_name)
        success, file_data = pb.upload_file(pic, message, 'image/jpeg',)

    upload_message = "{0} uploading picture {1} to url {2}".format(
        'Success' if str(success) else 'Failure',
        file_data.get('file_name'),
        file_data.get('file_url'))
    print(upload_message)
    devices = pb.devices

    if any([item in pushbullet_device_names for item in pushbullet_device_names]):
        for deviceName in pushbullet_device_names:
            device_list = [d for d in devices if d.nickname == deviceName and d.active]
            device = device_list[0] if device_list else None
            if device is not None:
                success, push = device.push_file(**file_data)
                print('Successfully pushed ' + push.get('iden') + ' to ' + device.nickname)
    else:
        success, push = pb.push_file(**file_data)
        print('Successfully pushed ' + push.get('iden') + ' to all devices')

    os.remove(file_path)

if __name__ == '__main__':
    # Being executed as a script
    config = SmartDoorConfig.read_config()
    take_photo_and_push(config['flip_pic_h'], config['flip_pic_v'], config['pushbullet_auth_key'], config['pushbullet_device_names'])
