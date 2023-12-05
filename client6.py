import socket
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np
import sys
import time
from naoqi import ALProxy

IP = "192.168.20.103"
PORT = 9559
camProxy = ALProxy("ALVideoDevice", IP, PORT)
resolution = 2    # VGA
colorSpace = 11   # RGB

def getimgfromnao(imgname):
	# -*- encoding: UTF-8 -*-
	# Get an image from NAO. save it using PIL.
	
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

	
	# Create a PIL Image from our pixel array.
	#print(type (face))
	#print(face)

	im = Image.frombytes("RGB", (imageWidth, imageHeight), array)



	# Save the image.    
	im.save(imgname, "PNG")
	pass

def createimage(imgname):
	#let's create a 6 x 6 matrix with all pixels in black color
	img = np.zeros((6,6,3),np.uint8)

	#let's use "for" cycle to change colorspace of pixel in a random way
	for x in range(6):
		for y in range(6):
			#We use "0" for black color (do nothing) 
			#and "1" for white color (change pixel value to [255,255,255])
			value = random.randint(0,1)
			if value == 1:
				img[x,y] = [255,255,255]

	#save our image as a "png" image
	cv2.imwrite(imgname,img)

def rpsclient():
	print 'hi at anytime enter 1 to break the loop'
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("1")

	client_socket.connect(('127.0.0.1', 65432))
	print("2")
	while True:
		outfilename=raw_input("enter out image name:")
		print("3")
		
		#createimage(outfilename)
		getimgfromnao(outfilename)

		port = client_socket.send(outfilename)

		data = client_socket.recv(4096)

		print("4")

		print data
		choice=raw_input("Next image, yes or no")
		if choice=="no":
			break

	client_socket.close()
	print("5")

def initialize():
	pass

	
if __name__ == '__main__':
	initialize()
	rpsclient()
