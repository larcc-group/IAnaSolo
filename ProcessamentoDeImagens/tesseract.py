import cv2
import sys
import pytesseract
import re

def readImage(path):

    # Read image path from command line
    imPath = path
    # Uncomment the line below to provide path to tesseract manually
    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    # Define config parameters.
    # '-l eng' for using the English language
    # '--oem 1' for using LSTM OCR Engine

    config = ('--oem 1 --psm 7')
    # config = ('--oem 0 --psm 7')

    # Read image from disk
    im = cv2.imread(imPath)

    # Run tesseract OCR on image
    text = pytesseract.image_to_string(im, config=config)

    text = text.replace('.',",")
    regex = r"[-]{0,1}[\d]*[\,]{0,1}[\d]+"
    newValues = re.findall(regex, text)

    while(len(newValues) <= 12):
        newValues.append("N.D")

    # Print recognized text
    print("TesseractResponse", text)

    return newValues