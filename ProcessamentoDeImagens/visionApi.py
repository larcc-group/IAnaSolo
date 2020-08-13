from google.cloud import vision
from google.cloud.vision import types
import os
import io
import tools
from enum import Enum
from PIL import Image, ImageDraw
import random
import re

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def sendSequentialGoogleVision(imagePaths, qtdSend=4, dirPath=os.getcwd()+"/"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= dirPath + "key.json"

    qtdAppend = 0
    valuesAppend = []
    valuesGoogleVision = []
    finalValues = []


    for idx, img in enumerate(imagePaths):

        if qtdAppend < qtdSend or idx == (len(imagePaths) - 1):
            qtdAppend += 1
            valuesAppend.append(img)
        else:
            imgMerge = tools.merge_image(valuesAppend,0,0,'white',False,"tabela"+ str(idx))
            valuesGoogleVision.append(imgMerge)
            valuesAppend.clear()
            valuesAppend.append(img)
            qtdAppend = 1

    if len(valuesAppend) > 0:
        imgMerge = tools.merge_image(valuesAppend,0,40,'white',False,"tabela")
        valuesGoogleVision.append(imgMerge)
        valuesAppend.clear()
        qtdAppend = 0

    values = []
    for gv in valuesGoogleVision:
        values.clear()
        values = sendToGoogleVision(gv)

        print("MY VAlues")
        print(values)
     
        for v in values:    
            split = v.split("\n")

            print("my values splited")
            print(split)
            for s in split:
                if s != '':
                    finalValues.append(s)
    
    try:
        finalValues.remove('')
    except:
        print("Nenhum valor vazio encontrado no retorno")
        
    return finalValues

def sendToGoogleVision(urlPath, img, convertToNumber=False, pathKey=os.getcwd()+"/"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= pathKey + "key.json"
    print(convertToNumber)

    client = vision.ImageAnnotatorClient()
    content = None

    if img != None:
        content = img
    elif urlPath != '':
    
        with io.open(urlPath, 'rb') as image_file:
            content = image_file.read()
    else:
        print("Nenhum imagem passada para o Vision")

    image = vision.types.Image(content=content)

    resp = client.document_text_detection(image=image)

    full_text_annotation = resp.full_text_annotation.text

    print("retorno", full_text_annotation)

    # print("retorno", get_document_bounds(resp.full_text_annotation, FeatureType.WORD))
    # hash = random.getrandbits(128)
    # render_doc_text(resp.full_text_annotation, urlPath, "resultado/return_"+str(hash)+".png")

    values = []
    newValues = []
    requestConfidence = 0

    text = full_text_annotation.replace('.',",")
    regex = r"[-]{0,1}[\d]*[\,]{0,1}[\d]+"
    newValues = re.findall(regex, text)

    print("Valores tratados")
    print(newValues)

    if len(newValues) > 0:
        requestConfidence = getConfidence(resp.full_text_annotation)

    while(len(newValues) <= 12):
        newValues.append("N.D")

    return newValues,requestConfidence


# def sendToGoogleVision(urlPath, img, convertToNumber=False, pathKey=os.getcwd()+"/"):
    
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= pathKey + "key.json"
    
#     print(convertToNumber)

#     client = vision.ImageAnnotatorClient()
#     content = None

#     if img != None:
#         content = img
#     elif urlPath != '':
#         with io.open(urlPath, 'rb') as image_file:
#             content = image_file.read()
#     else:
#         print("Nenhum imagem passada para o Vision")

#     image = vision.types.Image(content=content)

#     resp = client.document_text_detection(image=image)

#     full_text_annotation = resp.full_text_annotation.text

#     print("retorno", full_text_annotation)

#     # print("retorno", get_document_bounds(resp.full_text_annotation, FeatureType.WORD))
#     # hash = random.getrandbits(128)
#     # render_doc_text(resp.full_text_annotation, urlPath, "resultado/return_"+str(hash)+".png")

#     values = []
#     newValues = []
#     requestConfidence = 0

  
#     #     values = full_text_annotation.split(" ")  
        
#     #     for idx, val in enumerate(values):
#     #         split = val.split("\n")
#     #         for s in split:
#     #             newValues.append(s)

#     newValues = readBlocks(resp.full_text_annotation)

#     if convertToNumber == True:
#         try:
#             newValues[index] = int(newValues[index])
#         except:
#             print("Nenhum valor vazio encontrado!")    

#         for index, item in enumerate(newValues):
#             value = str(item)
#             if str(item).find(".", len(str(item))-1, len(item)) > 0:
#                 value = value.replace(".","",len(str(item))-1)
                
#             newValues[index] = value.replace(",",".")
#             try:
#                 newValues[index] = float(newValues[index])
#             except:
#                 newValues[index] = "N.D"

#     if len(newValues) > 0:
#         requestConfidence = getConfidence(resp.full_text_annotation)

#     return newValues,requestConfidence    

def readBlocks(text_annotation):
    newValues = []
 
    blocks = text_annotation.pages[0].blocks
    for block in blocks:
        blockValue = ''
        for p in block.paragraphs:
            for w in p.words:
                for s in w.symbols:
                    blockValue += str(s.text)
        newValues.append(blockValue)
    
    print(newValues)
    return newValues

def getConfidence(text_annotation):
    try:
        blocks = text_annotation.pages[0].blocks
        confidenceSum = 0
        for block in blocks:
            confidenceSum += block.confidence
        
        return confidenceSum/len(blocks)

    except:
        print("Ocorreu um erro ao obter a confidencia")


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image


def get_document_bounds(document, feature):
   
    bounds = []

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    # [END vision_document_text_tutorial_detect_bounds]
    return bounds


def render_doc_text(response, filein, fileout):
    image = Image.open(filein)
    # bounds = get_document_bounds(response, FeatureType.PAGE)
    # draw_boxes(image, bounds, 'blue')
    # bounds = get_document_bounds(response, FeatureType.PARA)
    # draw_boxes(image, bounds, 'red')
    bounds = get_document_bounds(response, FeatureType.WORD)
    draw_boxes(image, bounds, 'red')

    if fileout is not 0:
        image.save(fileout)
    else:
        image.show()