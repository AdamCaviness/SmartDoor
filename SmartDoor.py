import os
import re
import sys
import json
import picamera
import datetime
from pushbullet import PushBullet

# Implements pushbullet.py, see https://pypi.python.org/pypi/pushbullet.py
# Implements picamera.py, see http://raspberrypi.org/picamera-pure-python-interface-for-camera-module

executingPath = os.path.dirname(sys.argv[0])
configFileName = os.path.join(executingPath, "config.json")
    
with open(configFileName) as conf:
    config = json.load(conf)

fileName = datetime.datetime.now().strftime("%I:%M%p %m-%d-%Y") + ".jpg"
filePath = os.path.join("/home/pi", fileName)
with picamera.PiCamera() as camera:
    camera.start_preview()
    camera.vflip = True
    camera.hflip = True
    camera.resolution = (1024, 768)
    camera.capture(filePath)

pb = PushBullet(config["auth_key"])

with open(filePath, "rb") as pic:
    message = "SmartDoor " + re.sub(".png", "", fileName)
    success, file_data = pb.upload_file(pic, message, "image/jpeg")

print("Success uploading picture " + file_data.get("file_name") + " at url " + file_data.get("file_url") + " " + str(success))
success, push = pb.push_file(**file_data)
print(push.get("iden") + " succeeded")
os.remove(filePath)


