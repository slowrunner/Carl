#!/usr/bin/env python3

"""
# filename: file_vision_text.py

# usage:
 - raspistill -o image.jpg
 - ./file_vision_label.py -i image.jpg

read an the passed image filename
convert to GoogleCloudVision image
create a request
send to google cloud
print text found in the image


Example run: ./file_vision_text.py -i carl_dock.jpg
Text:

"""


from google.cloud import vision
import argparse


client = vision.ImageAnnotatorClient()



def main():
    

    """Run a text request on a single image"""
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to image file")
    args = vars(ap.parse_args())
    filename = args['image']

    with open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
            for vertex in text.bounding_poly.vertices])
        print('bound: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                 response.error.message))


if __name__ == '__main__':

    main()
