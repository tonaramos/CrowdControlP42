import boto3
import numpy as np
import cv2

cap = cv2.VideoCapture('fan.mp4')
with open('rootkey.csv', 'r') as creds:
   creds = creds.read().split()
   access_key_id = creds[0]
   secret_access_key = creds[1]

client = boto3.client('rekognition',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key)

while(cap.isOpened()):
   ret, photo = cap.read()

   cv2.imwrite('frame.jpg', photo)

   with open('frame.jpg', 'rb') as source_image:
       source_bytes = source_image.read()

   response = client.detect_faces(Image={'Bytes': source_bytes}, Attributes=['ALL'])



   counter = 0

   for faceDetail in response['FaceDetails']:
       counter += 1

   cv2.putText(photo, str(counter), (0,500), fontColor=(255,255,255))

   cv2.imshow('Window', photo)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()