# echo-server.py

import socket
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
from rps1 import detect

def showimg(imgfname):
	ifns=imgfname.decode("utf-8")
	img = mpimg.imread("c:\\python271\\"+ifns)
	imgplot = plt.imshow(img)
	#plt.show()
	#ifns="face.png"
	#image= cv2.imread("c:\\python271\\"+ifns)

	#plt.imshow(image)
	#plt.show()
	detect("c:\\python271\\"+ifns)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            imgfilename = conn.recv(1024)
            if not imgfilename:
                break

            print ("From client: ", imgfilename)
            showimg(imgfilename)
            conn.sendall("Processed! next?".encode('utf-8'))