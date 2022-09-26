#this script attempts to crop the image to isolate the location for more accurate transfer to the organized text docs

#written by Collin Dixon

from cgitb import text
from turtle import left, right
import numpy as np
import pytesseract
import argparse
import imutils
import cv2
from pdf2image import convert_from_path
import os
import sys



def ocr_core(file_name_here,psm):
    sconfig='--psm '+str(psm)
    try:
        text = pytesseract.image_to_string(file_name_here,
        config=sconfig)
    except:
        text='failed'
    return text

def readncrop(file_name):
    myimg=cv2.imread(file_name)[0:400,0:315]
    return myimg

def getfilenumber(file_name):
    return file_name.split('.')[0]

directory='/project/arcc-students/cdixon15/radiocarbon_project/cleanedimagesonly'
for folder in os.listdir(directory):
    newdir=directory+'/'+folder
    if os.path.isdir(newdir):
        os.makedirs('/project/arcc-students/cdixon15/radiocarbon_project/locationOCR/'+folder, exist_ok=True)
        for file in os.listdir(newdir):
            file_name=file
            test=readncrop(newdir+'/'+file)
            cv2.imwrite('/project/arcc-students/cdixon15/radiocarbon_project/locationscropped'+'/'+str(getfilenumber(file_name))+'.jpg',test)
            ocr=ocr_core(test,11)

            output_writer = open('/project/arcc-students/cdixon15/radiocarbon_project/locationOCR/'+folder+'/'+str(getfilenumber(file_name))+'.txt', "w+")

            output_writer.write(ocr)
