# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from PyQt5 import QtCore, QtGui, QtWidgets
#import mysql.connector
import tkinter as tk
import os
from PIL import Image
#import win32com.client
import csv
import re
import string
import operator
import numpy as np
from PyQt5.QtGui import QIcon, QPixmap
# construct the argument parse and parse the arguments
'''ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())'''
# load the example image and convert it to grayscale

#image = cv2.imread("example_01.png")

# check to see if we should apply thresholding to preprocess the
# image
'''if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)'''
 
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file

class ocr_english(object):
    def setupUi(self, Form):
        root = tk.Tk()
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.left = 0
        self.top = 0
        print(self.width, self.height)
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        Form.setObjectName("Form")
        Form.resize(self.width, self.height)
        Form.setMouseTracking(True)
        Form.setAutoFillBackground(True)
        
        p = Form.palette()
        p.setColor(Form.backgroundRole(), QtGui.QColor(188, 196, 195))
        Form.setPalette(p)

        #Form.setStyleSheet("background-color : rgb(47,76,122)");


        self.label= QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(800, 30, 700, 50))
        self.label.setText("OCR generation")
        self.label.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Black))

        
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(730, 70, 361, 70))
        self.label1.setText("Select text file")
        self.label1.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.imageLabel=QtWidgets.QLabel(Form)
                
        self.addNameButton=QtWidgets.QPushButton(Form)
        self.addNameButton.setGeometry(QtCore.QRect(950,90,93,28))
        self.addNameButton.setObjectName("addNameButton")
        self.audlineEdit = QtWidgets.QTextEdit(Form)
        self.audlineEdit.setGeometry(QtCore.QRect(900, 130, 400, 600))
        self.audlineEdit.setObjectName("audlineEdit")
        
        


        self.objpushButton = QtWidgets.QPushButton(Form)
        self.objpushButton.setGeometry(QtCore.QRect(650, 850, 150, 50))
        self.objpushButton.setObjectName("objpushButton")


        self.addNameButton.clicked.connect(self.setImage1)
        #self.audpushButton.clicked.connect(self.setAudio)
        self.objpushButton.clicked.connect(self.additem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addNameButton.setText(_translate("Form","Browse"))
        #self.audpushButton.setText(_translate("Form", "Add audio"))
        self.objpushButton.setText(_translate("Form", "Generate ocr"))

    def setImage1(self):
        global ifileName
        ifileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "/home/anika/Downloads", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        #image_name="niloy.jpg"
        image = cv2.imread(ifileName)
        width = int(image.shape[1])
        height = int(image.shape[0])
        print(width)
        print(height)
        pixmap = QPixmap(ifileName)
        self.imageLabel.setGeometry(QtCore.QRect(300, 130, 600,600))
        pixmap = pixmap.scaledToWidth(600)
        pixmap = pixmap.scaledToHeight(600)
        self.imageLabel.setPixmap(pixmap)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)


    def deleting(self):
        #self.imgLabel.clear()
        self.imglineEdit.setText("")
        self.imglineEdit2.setText("")
        self.imglineEdit3.setText("")
        #self.VideoLabel.clear()
        self.vidlineEdit.setText("")
        #self.audioLabel.clear()
        self.audlineEdit.setText("")
        self.addName.setText("")

        '''text = pytesseract.image_to_string(Image.open(filename))
#os.remove(filename)
f= open("outputimagetess.txt","a+")
print(text)
f.write(text)
f.close()
# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)'''

    def additem(self):
        import pandas as pd
        #convertDocToPdf(DOC_FILEPATH)
       
                
        original_image = cv2.imread(ifileName)
        height, width, channel = original_image.shape
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        blur_image = cv2.blur(gray_image, (3, 3))
        #edges = cv2.Canny(blur_image, 50, 150, apertureSize=3)

        th1 = cv2.adaptiveThreshold(blur_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # return value: a set of rho, theta values
        # parameter 1: input image -- the thresholded one
        # parameter 2: value for rho in pixels
        # parameter 3: value for theta
        # parameters 2 and 3 are used to get the votes in discrete intervals
        # parameter 4: the minimum number of pixels you need on a line to consider it a line
        # -- here I'm saying we need at least 0.5 (or 50%) pixels to be on the line
        hough_lines = cv2.HoughLines(th1, 1, np.pi / 180.0, int(width * 0.5))

        cv2.imshow('Original Image', original_image)
        cv2.imshow('Thresholded Image', th1)

        # we run through each lines and plot them on the original image
        for i in range(len(hough_lines)):
            for rho, theta in hough_lines[i]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                print(rho, theta, x1, y1, x2, y2)
                cv2.line(original_image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        #filename = ".png".format(os.getpid())
        cv2.imshow('Hough Transform Lines', original_image)
        text = pytesseract.image_to_string(Image.open(ifileName), lang='ben')
        #os.remove(filename)
        f= open("outputimagebengali.txt","w+")
        print(text)
        f.write(text)
        f.close()
        
        text=open('outputimagebengali.txt').read()
        self.audlineEdit.setText(text)
        # show the output images
        #cv2.imshow("Image", image)
        #cv2.imshow("Output", gray)
        cv2.waitKey(0)


if __name__ == "__main__":
    import sys
    ifileName=""
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ocr_english()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

