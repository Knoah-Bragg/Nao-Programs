# -*- encoding: UTF-8 -*-
# Get an image from NAO. Display it and save it using PIL.

import sys
import time

# Python Image Library
from PIL import Image
import numpy
from naoqi import ALProxy

import cv2
import matplotlib.pyplot as plt

def showNaoImage(IP, PORT):
  """
  First get an image from Nao, then show it on the screen with PIL.
  """

  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

  t0 = time.time()

  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageRemote(videoClient)

  t1 = time.time()

  # Time the image transfer.
  print "acquisition delay ", t1 - t0

  camProxy.unsubscribe(videoClient)

  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]

  # Face detection (load)
  face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

  # Create a PIL Image from our pixel array.
  for i in range(4):
    
    #print(type (face))
    #print(face)

    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    open_cv_image = numpy.array(im) 

    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    #cv2.imshow("Display window"+str(i), open_cv_image )
    # Face detection (execute)
    # Convert image to gray scale
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    #gray_image.shape
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    if len(face) > 0:
      tts = ALProxy("ALTextToSpeech", "192.168.20.103", 9559)
      tts.say("Hello! you are "+ str(len(face))+ " people!")
    for (x, y, w, h) in face:
      print(x, y, w, h)
      cv2.rectangle(gray_image, (x, y), (x + w, y + h), (0, 255, 0), 4)

    # Convert back to rgb
    img_rgb = cv2.cvtColor(gray_image, cv2.COLOR_BGR2RGB)

    # Display image
    plt.figure(figsize=(20,10))
    plt.imshow(img_rgb)
    plt.axis('off')
    #plt.show()

    # Save the image.
    iname="camImage2811" +str(i)+".png"
    giname="camImageg2811" +str(i)+".png"
    print(iname)
    
    im.save(iname, "PNG")
    cv2.imwrite(giname,img_rgb)
    print(type(im))
    print(im)
  k = cv2.waitKey(0) # Wait for a keystroke in the window

  #im.show()

if __name__ == '__main__':
  IP = "192.168.20.103"  # Replace here with your NaoQi's IP address.
  PORT = 9559

  # Read IP address from first argument if any.
  if len(sys.argv) > 1:
    IP = sys.argv[1]

  naoImage = showNaoImage(IP, PORT)
