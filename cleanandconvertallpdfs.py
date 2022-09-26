
#this script is meant to clean, crop, and convert all images to text.
#it uses cv2 to clean and crop the image and pytesseract to perform OCR on the images
#large parts of code taken from https://pyimagesearch.com/2021/11/22/improving-ocr-results-with-basic-image-processing/

#written by Collin Dixon

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

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to image")g 
#args = vars(ap.parse_args())

# load the input image and convert it to grayscale
largedir='/project/arcc-students/cbray3/radiocarbon_card_copies/ocr'
for folder in os.listdir('/project/arcc-students/cbray3/radiocarbon_card_copies/ocr'):
    directory=largedir+'/'+folder
    for file in  os.listdir(directory):
        try:
            pdfimage=directory+'/'+file
            image=convert_from_path(pdfimage)

            
            image[0].save('/project/arcc-students/cdixon15/radiocarbon_project/test.jpg','jpeg')

            image=cv2.imread('/project/arcc-students/cdixon15/radiocarbon_project/test.jpg')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # threshold the image using Otsu's thresholding method
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/thresh.jpg", thresh)

            # apply a distance transform which calculates the distance to the
            # closest zero pixel for each pixel in the input image
            dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
            # normalize the distance transform such that the distances lie in
            # the range [0, 1] and then convert the distance transform back to
            # an unsigned 8-bit integer in the range [0, 255]
            dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
            dist = (dist * 255).astype("uint8")
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/dist.jpg", dist)


            
            #_________________________________________________________________________________________________
            #here we are cropping the image based on where the border punches are
            #using this otsu threshhold to help find where to crop the image could be very promising

            # threshold the distance transform using Otsu's method
            dist = cv2.threshold(dist, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/distotsu.jpg", dist)

            #change this bordersize to change all slices
            #essentially we take slices of each side and find 
            #the farthest pixel towards the opposite side of the side they were taken from
            bordersize=120
            leftslice=dist[0+bordersize:dist.shape[0]-120,0:120]
            leftmaxarray=np.where((leftslice != 0).any(axis=0))[0]
            leftmax=int(leftmaxarray[-1])
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/left.jpg", leftslice)
            rightslice=dist[0+bordersize:dist.shape[0]-120,dist.shape[1]-120:dist.shape[1]]
            rightmaxarray=np.where((rightslice != 0).any(axis=0))[0]
            rightmax=int(rightmaxarray[0]+dist.shape[1]-120)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/right.jpg", rightslice)
            topslice=dist[0:bordersize,bordersize:dist.shape[1]-120]
            topmaxarray=np.where((topslice != 0).any(axis=1))[0]
            topmax=int(topmaxarray[-1])
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/top.jpg", topslice)
            bottomslice=dist[dist.shape[0]-120:dist.shape[0],0:dist.shape[1]-120]
            bottommaxarray=np.where((bottomslice != 0).any(axis=1))[0]
            bottommax=int(bottommaxarray[0]+dist.shape[0]-120)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/bottom.jpg", bottomslice)

            #now we know where to crop using these max values!
            #we now essentially restart the process, this time cropping first
            pdfimage=directory+'/'+file
            image=convert_from_path(pdfimage)


            image[0].save('/project/arcc-students/cdixon15/radiocarbon_project/test.jpg','jpeg')

            image=cv2.imread('/project/arcc-students/cdixon15/radiocarbon_project/test.jpg')
            image = image[topmax:bottommax, leftmax:rightmax]

            #_________________________________________________________________________________________________

            #time to start again this time with a nicely cropped image
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/testcropped.jpg", image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # threshold the image using Otsu's thresholding method
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/thresh.jpg", thresh)

            # apply a distance transform which calculates the distance to the
            # closest zero pixel for each pixel in the input image
            dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
            # normalize the distance transform such that the distances lie in
            # the range [0, 1] and then convert the distance transform back to
            # an unsigned 8-bit integer in the range [0, 255]
            dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
            dist = (dist * 255).astype("uint8")
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/dist.jpg", dist)

            #using this otsu threshhold to help find where to crop the image could be very promising

            # threshold the distance transform using Otsu's method
            dist = cv2.threshold(dist, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/distotsu.jpg", dist)

            # apply an "opening" morphological operation to disconnect components
            # in the image
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
            opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/opening.jpg", opening)

            # find contours in the opening image, then initialize the list of
            # contours which belong to actual characters that we will be OCR'ing
            cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            chars = []
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour
                (x, y, w, h) = cv2.boundingRect(c)
                # check if contour is at least 35px wide and 100px tall, and if
                # so, consider the contour a digit
                if w >= 5 and h >= 5:
                    chars.append(c)

            # compute the convex hull of the characters
            chars = np.vstack([chars[i] for i in range(0, len(chars))])
            hull = cv2.convexHull(chars)
            # allocate memory for the convex hull mask, draw the convex hull on
            # the image, and then enlarge it via a dilation
            mask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.drawContours(mask, [hull], -1, 255, -1)
            mask = cv2.dilate(mask, None, iterations=2)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/mask.jpg", mask)
            # take the bitwise of the opening image and the mask to reveal *just*
            # the characters in the image
            final = cv2.bitwise_and(opening, opening, mask=mask)
            filenumber=file.split(".")[0]
            os.makedirs('/project/arcc-students/cdixon15/radiocarbon_project/cleanedimages/'+directory.split('/')[-1], exist_ok=True)
            cv2.imwrite('/project/arcc-students/cdixon15/radiocarbon_project/cleanedimages/'+directory.split('/')[-1]+'/'+str(filenumber)+".jpg", final)
            print(filenumber)

            text=ocr_core('/project/arcc-students/cdixon15/radiocarbon_project/cleanedimages/'+directory.split('/')[-1]+'/'+str(filenumber)+".jpg", 11)
        except BaseException as ex:
            text=str(ex)
        os.makedirs('/project/arcc-students/cdixon15/radiocarbon_project/cleanedtesseractOCR/'+directory.split('/')[-1], exist_ok=True)
        output_writer = open('/project/arcc-students/cdixon15/radiocarbon_project/cleanedtesseractOCR/'+directory.split('/')[-1]+'/'+str(filenumber)+'.txt', "w")
        output_writer.write(text)