# Test of Google Cloud Vision On The Raspberry Pi (no GoPiGo3 calls


Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera. 
 
https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Uses Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and 
classify it with the Google Cloud Vision API.   

1) Take a picture
2) convert it to a standard Google Cloud Vision image format
3) Create a request with the the GCV formatted image
4) Send the request (to use particular Vision API)
 - logo - python3 camera_vision_logo.py
 - objects - python3 camera_vision_label.py
 - facial expressions  - python3 camera_vision_face.py
5) print out the json result

file_vision_label.py takes a jpg image and sends it up for labeling:
```
./file_vision_label.py -i wheel.jpg

Labels:
Tire
Automotive tire
Yellow
Wheel
Rim
Auto part
Automotive wheel system
Synthetic rubber
Tire care

```
The difficult part about this was setting up the Google Cloud stuff.  I already had a project from the Google AIY Voice Kit several years ago, but ended up having to:

- create a new project
- enable the vision API for the project
- create a new credential-service_account-project-Owner-internal-JSON for the project
- create a new billing account
- link the billing account to the service_account
- download the JSON credential file to my mac
- copy contents of JSON credential file to RPI file  /home/pi/Carl/Examples/GoogleCloudVision/google.cloud.cred.json


The software installation on the my RPI:
```
mkdir /home/pi/Carl/Examples/GoogleCloudVision/
python3 -m pip install --user google-cloud-vision
python3 -m pip install --user Pillow
python3 -m pip install --user picamera
sudo nano ~/.bashrc
added: export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Carl/Examples/GoogleCloudVision/google.cloud.cred.json"
source ~/.bashrc
more $GOOGLE_APPLICATION_CREDENTIALS
cd ~/Carl/Examples/GoogleCloudVision/
git clone https://github.com/DexterInd/GoogleVisionTutorials
cp GoogleVisionTutorials/*.py .
cp GoogleVisionTutorials/wheel.py .
created a README.md from the GoogleVisionTutorials/README.md

```
