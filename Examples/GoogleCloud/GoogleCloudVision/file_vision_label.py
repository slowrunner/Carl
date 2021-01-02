#!/usr/bin/env python3

"""
# filename: file_vision_label.py

# usage:
 - raspistill -o image.jpg
 - ./file_vision_label.py -i image.jpg

read an the passed image filename
convert to GoogleCloudVision image 
create a request
send to google cloud 
print labels found in the image


Example run: ./file_vision_label.py -i wheel.jpg
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

"""


from google.cloud import vision
import argparse


client = vision.ImageAnnotatorClient()



def main():
    

    """Run a label request on a single image"""
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to image file")
    args = vars(ap.parse_args())
    filename = args['image']

    with open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)


    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

if __name__ == '__main__':

    main()
