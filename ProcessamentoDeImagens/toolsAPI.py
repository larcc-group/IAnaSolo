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

def initial_tratment(dirpath, src):

    command = dirpath + 'textcleaner'
    input_file = dirpath + "/" + src
    params = '-g -e stretch -f 15 -o 3 -t 5 -u -s 1 -T -p 20'
    output_file  = dirpath + '/resultAdjust.jpg'
    finalCommand = command + " " + params + " " + input_file + " " + output_file

    with open('log.json', 'w') as json_file:
        json.dump(finalCommand, json_file)

    print(finalCommand)
    os.system(finalCommand)

    command = dirpath + 'noisecleaner'
    params = '-m 1 -n 4'
    output_file  = dirpath + '/resultAdjust.jpg'
    finalCommand = command + " " + params + " " + output_file + " " + output_file

    print(finalCommand)
    os.system(finalCommand)

    command = dirpath + 'textdeskew'
    params = ''
    output_file  = dirpath + '/resultAdjust.jpg'
    finalCommand = command + " " + params + " " + output_file + " " + output_file

    print(finalCommand)
    os.system(finalCommand)

    command = 'convert'
    params = '-flatten -fuzz 1% -trim'
    output_file  = dirpath + '/resultAdjust.jpg'
    finalCommand = command + " " + output_file + " " + params + " " + output_file

    print(finalCommand)
    os.system(finalCommand)

    return output_file

def create_csv(json):
    analises = json.loads(json)
    f = csv.writer(open("analises.csv", "wb+"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["Cliente","Local","Fazenda","Gleba","Área","Data(dd/mm/aaaa)","Nº_Análise","pH","Ca (cmolc/dm³)","Mg (cmolc/dm³)","Al (cmolc/dm³)","H + Al (cmolc/dm³)","SMP","MO (%)","Argila (%)","P (mg/dm³)","K (mg/dm³)","Condição_área","Extração_P"])

    for idx, analise in enumerate(analises):
        f.writerow([analise["Nome"] + "TCC_" + str(idx),
                    analise["Localidade"] + "Local_" + str(idx),
                    "Municipio Teste",
                    "Soja" + str(idx),
                    analise["dadosExtraidos"]["area_ha"],
                    analise["Data_Recebimento"],
                    analise["dadosExtraidos"]["amostra"],
                    analise["dadosExtraidos"]["ph_H20"],
                    analise["dadosExtraidos"]["ca"],
                    analise["dadosExtraidos"]["mg"],
                    analise["dadosExtraidos"]["al"],
                    analise["dadosExtraidos"]["h_al"],
                    analise["dadosExtraidos"]["indice_SMP"],
                    analise["dadosExtraidos"]["mo"],
                    analise["dadosExtraidos"]["argila"],
                    analise["dadosExtraidos"]["p"],
                    analise["dadosExtraidos"]["k"],
                    analise["dadosExtraidos"]["classe_textural"],
                    "1" ])
        
def resizeImage(img, widthResize):
    width = img.shape[1]
    height = img.shape[0]
    proportion = float(height/width)
    new_width = widthResize# in pixels
    new_height = int(new_width*proportion)
    new_size = (new_width, new_height)
    resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    return resized_img

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


def merge_image(pathImagesArray, shuffle = 0, padding = 0, bgColor='white', vertically = False, pathName = ''):
    
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
        for im in images:
            new_im.paste(im, (x_offset, shuffle))

            if shuffle == 0:
                shuffle = auxShuffle
            else:
                shuffle = 0   

            x_offset += im.size[0] + padding

    byteIO = io.BytesIO()
    new_im.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()

    # new_im.save(os.getcwd() + '/googleVision/' +pathName + '.jpg')

    return byteArr
