import boto3
import numpy as np
import cv2
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor

with open('rootkey.csv', 'r') as creds:
   creds = creds.read().split()
   access_key_id = creds[0]
   secret_access_key = creds[1]

client = boto3.client('rekognition',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key)

s3_connection = boto3.resource('s3',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
s3_object = s3_connection.Object('calixbucket2','crowd2.jpg')
s3_response = s3_object.get()
stream = io.BytesIO(s3_response['Body'].read())
image=Image.open(stream)
imgWidth, imgHeight = image.size
draw = ImageDraw.Draw(image)

with open('crowd2.jpg', 'rb') as source_image:
   source_bytes = source_image.read()

response = client.detect_faces(Image={'Bytes': source_bytes}, Attributes=['ALL'])

counter = 0

for faceDetail in response['FaceDetails']:
   box = faceDetail['BoundingBox']
   left = imgWidth * box['Left']
   top = imgHeight * box['Top']
   width = imgWidth * box['Width']
   height = imgHeight * box['Height']
   points = (
       (left,top),
       (left + width, top),
       (left + width, top + height),
       (left , top + height),
       (left, top)

   )
   draw.line(points, fill='white', width=2)
   counter += 1

image.show()
print(counter)