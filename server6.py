# echo-server.py

import socket
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

scores = [0, 0]  # [AI, Player]

def detect(fn):
    global scores

    imgBG = cv2.imread("C:\\Users\\don\\server\\Resources\\BG.png")
    if imgBG is None:
          print("Error: Unable to load the background image.")
          return -20

    detector = HandDetector(maxHands=1)

    timer = 0
    stateResult = False
    startGame = False
    
    flag=0

    img=cv2.imread(fn)
    imgScaled = cv2.resize(img, (480, 420), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if hands:
      playerMove = None
      hand = hands[0]
      fingers = detector.fingersUp(hand)
      print(fingers)
      if fingers == [0, 0, 0, 0, 0]:
         playerMove = 1
      if fingers == [1, 1, 1, 1, 1]:
         playerMove = 2
      if fingers == [0, 1, 1, 0, 0]:
         playerMove = 3

      randomNumber = random.randint(1, 3)
      tm="Resources\\"+str(randomNumber)+".png"
      print (tm)
      imgAI = cv2.imread(tm, cv2.IMREAD_UNCHANGED)
      imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

      print (playerMove, randomNumber)

      # Player Wins
      if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
         scores[1] += 1
         print("player wins")
         flag=1   

      # AI Wins
      if (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
         scores[0] += 1
         print("ai wins")
         flag=2

      imgBG[234:654, 795:1195] = imgScaled

      imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

      cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
      cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

      cv2.imshow("BG", imgBG)
      cv2.waitKey(0)
      return flag

def showimg(imgfname):
	ifns=imgfname.decode("utf-8")
	img = mpimg.imread("c:\\python271\\"+ifns)
	
	flag = detect("c:\\python271\\"+ifns)
	print("in server", flag)

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
