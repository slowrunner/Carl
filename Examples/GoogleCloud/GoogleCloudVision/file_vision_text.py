#!/usr/bin/env python3

"""
# filename: file_vision_text.py

# usage:
 - raspistill -o image.jpg
 - ./file_vision_text.py -i image.jpg

read an the passed image filename
convert to GoogleCloudVision image
create a request
send to google cloud
print text found in the image


Example run: ./file_vision_text.py -i carl_dock.jpg

Texts:

"CARL
Cute and Real Lovable
"
bound: (862,930),(1345,930),(1345,1094),(862,1094)

"CARL"
bound: (864,930),(1345,936),(1343,1067),(862,1061)

"Cute"
bound: (973,1072),(1028,1072),(1028,1091),(973,1091)

"and"
bound: (1038,1073),(1081,1073),(1081,1092),(1038,1092)

"Real"
bound: (1093,1072),(1145,1072),(1145,1092),(1093,1092)

"Lovable"
bound: (1157,1073),(1249,1074),(1249,1094),(1157,1093)

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
