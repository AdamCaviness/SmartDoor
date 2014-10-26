SmartDoor
========

Add a little security and comfort to your front door.  When someone rings your doorbell, recieve a photo of that person
on your smartphone or web browser via PushBullet.  In today's world sometimes you may not want to go to the door.
A Raspberry Pi is used to take the photo and your existing doorbell acts as the sensor input.

### Configuration
A config.json file is required and a sample structure is provided in configsample.json.
You will need to get a PushBullet API Key from your PushBullet account settings and update your config.json file.
You may supply an array of device nicknames to send your pushes to or leave the array blank [] and all your devices will receive the push.
Currently the GPIO pins are configured as per BCM (Broadcom) spec instead of the pin number layout of BOARD.

### Contributions
Any bug fixes or improvements are welcomed and appreciated.  Request a pull into the master if you like.

### Licensing
SmartDoor is released under the [MIT license](http://opensource.org/licenses/mit-license.php).
