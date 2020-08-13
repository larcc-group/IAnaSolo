# -*- coding: utf-8 -*-

from __future__ import print_function
import cv2
import numpy as np
from PIL import Image
from os import walk
import os
import sys
import io
import json
import csv
from wand.image import Image as Img
from wand.color import Color
import shutil
import visionApi
from shutil import copyfile
from unidecode import unidecode

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

class Generic:
     def __init__(self, x):
         self.x = x

def resizeImage(path, widthResize):
    command = 'convert'
    params = '-resize '+str(widthResize)+'x'
    output_file  = path
    finalCommand = command + " " + output_file + " " + params + " " + output_file

    # print(finalCommand)
    os.system(finalCommand)

def pdfToImage(input_path, output):

    with Img(filename=input_path, resolution=300) as img:
        img.background_color = Color('white') # Set white background.
        img.alpha_channel = 'remove' 

        with img.convert('png') as converted:
            converted.save(filename=output)

            return output

def textCleaner(inputPath,outputPath):
    command = './textcleaner'
    input_file = inputPath
    params = '-g -e normalize'
    # params = '-g -e normalize -f 20 -o 11'
    output_file  = outputPath
    finalCommand = command + " " + params + " " + input_file + " " + output_file

    os.system(finalCommand)

def textCleaner2(inputPath,outputPath):
    command = './textcleaner'
    input_file = inputPath
    params = '-g -e stretch -f 20 -o 2 -t 7 -s 1 -T -p 20'
    # params = '-g -e normalize -f 15 -o 10'
    output_file  = outputPath
    finalCommand = command + " " + params + " " + input_file + " " + output_file

    os.system(finalCommand)

def textCleaner3(inputPath,outputPath):
    command = './textcleaner'
    input_file = inputPath
    params = '-e normalize -f 15 -o 5 -S 200 -s 1'
    # params = '-g -e normalize -f 15 -o 10'
    output_file  = outputPath
    finalCommand = command + " " + params + " " + input_file + " " + output_file

    os.system(finalCommand)


def textDeskew(path):
    command = './textdeskew'
    params = ''
    finalCommand = command + " " + params + " " + path + " " + path

    os.system(finalCommand)

def levelTratment(inputoutput):
    command = 'convert'
    params = '-colorspace Lab -channel 0 -auto-level +channel -colorspace sRGB'
    finalCommand = command + " " + inputoutput + " " + params + " " + inputoutput

    # print(finalCommand)
    os.system(finalCommand)


def initial_tratment(inputPath, outputPath):

    command = 'convert'
    params = '-interlace Plane -gaussian-blur 0.05 -quality 100%'
    finalCommand = command + " " + params + " " + inputPath + " " + outputPath

    # print(finalCommand)
    os.system(finalCommand)

    command = './textdeskew'
    params = ''
    finalCommand = command + " " + params + " " + outputPath + " " + outputPath

    # print(finalCommand)
    os.system(finalCommand)

    command = 'convert'
    params = '-fuzz 20% -trim -trim -bordercolor white -border 1x1'
    finalCommand = command + " " + outputPath + " " + params + " " + outputPath

    # print(finalCommand)
    os.system(finalCommand)

    levelTratment(outputPath)

    textCleaner2(outputPath,outputPath)

    resizeImage(outputPath,1024)

    return outputPath

def imagenegatetratment(inputpath, outputPath):
    command = 'convert'
    params = '-level 0%,90%,0.5'
    params = '-alpha off'
    output_file  = outputPath
    finalCommand = command + " " + output_file + " " + params + " " + output_file

    # print(finalCommand)
    os.system(finalCommand)

    resizeImage(output_file,1024)

    return outputPath


def alphatratament(inputpath, outputPath):
    command = 'convert'
    params = '-alpha off'
    output_file  = outputPath
    finalCommand = command + " " + output_file + " " + params + " " + output_file

    # print(finalCommand)
    os.system(finalCommand)

    resizeImage(output_file,1024)

    return outputPath


def removeTemporaryFiles(directory):
    shutil.rmtree(directory)

def vars2(obj):
    try:
        return vars(obj)
    except TypeError:
       return {k: getattr(obj, k) for k in obj.__slots__}

def extractCover(pathCover, keysResultValuesJson):

    extractCapaValues, confidence = visionApi.sendToGoogleVision(pathCover,None)

    splitKeyValue = extractCapaValues.split("\n")

    for idx, capaItem in enumerate(splitKeyValue):    
        itemSplit = capaItem.split(":")
        if(len(itemSplit) == 2): #key, value
            for prop in keysResultValuesJson:
                if(prop == unidecode(itemSplit[0].replace(" ",""))):
                    keysResultValuesJson[prop] = itemSplit[1]

    return keysResultValuesJson


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


def merge_image(pathSave, pathImagesArray, shuffle = 0, padding = 0, bgColor='white', vertically = False, pathName = ''):

    images = list(map(Image.open,pathImagesArray))

    auxShuffle = shuffle
    widths, heights = zip(*(i.size for i in images))

    if padding > 0:
        Lheights = list(heights)
        LWidths = list(widths)

        for idx, h in enumerate(Lheights):
            Lheights[idx] = h + padding
        
        for idx, w in enumerate(LWidths):
            LWidths[idx] = w + padding

        heights = tuple(Lheights)
        widths = tuple(LWidths)

    if vertically:
        max_width = max(widths) + shuffle + padding
        total_height = sum(heights) + padding
        new_im = Image.new('RGB', (max_width, total_height), color=bgColor)

        y_offset = padding
        for im in images:
            new_im.paste(im, (shuffle, y_offset))

            if shuffle == 0:
                shuffle = auxShuffle
            else:
                shuffle = 0    

            y_offset += im.size[1] + padding
    else:
        total_width = sum(widths) + padding
        max_height = max(heights) + shuffle + padding
        new_im = Image.new('RGB', (total_width, max_height), color=bgColor)

        x_offset = padding
        y_offset = padding
        for im in images:
            new_im.paste(im, (x_offset, y_offset))

            if shuffle == 0:
                shuffle = auxShuffle
            else:
                shuffle = 0   

            x_offset += im.size[0] + padding

    byteIO = io.BytesIO()
    new_im.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()

    fullPath = pathSave + "/" + pathName + '.jpg'

    new_im.save(fullPath)

    return fullPath
 

def removeBorder(inputFile):
    command = 'convert'
    input_file = inputFile
    params = '-shave 2x2'
    output_file  = inputFile
    finalCommand = command + " " + input_file + " " + params + " " + output_file
    os.system(finalCommand)

def addBorder(inputFile, size, color):
    command = 'mogrify'
    input_file = inputFile
    params = '-shave 1x1 -bordercolor white -border 30' 
    output_file  = inputFile
    finalCommand = command + " " + params + " " + input_file + " " + output_file
    os.system(finalCommand)

def setOnWhiteDocument(pathBg, pathCrop):
    command = 'composite'
    params = '-gravity Center'
    output_file  = pathCrop
    finalCommand = command + " " + params + " " + pathCrop + " " + pathBg + " " + output_file
    os.system(finalCommand)

def findCenter(gray):

    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    _, cnts = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(cnts[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)
 
def create_csv(analises, outFile):

    with open('outFile', 'w+', encoding='utf8') as f:
        csvFile = csv.writer(f)
    # csvFile = csv.writer(open(outFile, "w+", encoding='utf8'))

    # Write CSV Header, If you dont need that, remove this line
        
        headerCSV = []
        contentCSV = []
        
        if len(analises) > 0:
            for idx, analise in enumerate(analises):
                headerCSV = []
                contentCSV = []
                for prop in analise:
                    if prop != "dadosExtraidos":
                        if idx == 0: # primeira analise
                            headerCSV.append(prop)

                        contentCSV.append(analise[prop])
                    else:
                        for propExtract in analise["dadosExtraidos"]:
                            if idx == 0: # primeira analise
                                headerCSV.append(propExtract)

                            contentCSV.append(analise["dadosExtraidos"][propExtract])

                if len(headerCSV) > 0:
                    csvFile.writerow(headerCSV)    
                
                csvFile.writerow(contentCSV)  
        else:
            print("Nenhuma informação disponível para gerar o arquivo CSV") 

    

        
