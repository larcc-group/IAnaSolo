# -*- coding: utf-8 -*-

from _json import make_encoder
import cv2
from numpy import block
import tools
import visionApi
import tesseract
import numpy as np
import os
import random
import time
import json
import sys
from PIL import Image
from io import StringIO
from os import walk
from shutil import copyfile, move

import _thread
import threading


# Global variables
capaCrop = None
checkCapa = False
__dirpath= os.getcwd()
__resultsDirectory = __dirpath + "/results"
__successDirectory = __dirpath + "/successFiles"
__errorDirectory = __dirpath + "/errorFiles"
__googleVisionDirectory = __dirpath + "/googleVision"

class ProcessResult(object):
    tables = []
    content = None
    cover = []

def ReadAdjustImage(index, location, sequentialSend, numberSequentials, orderMethod, makeBlur, blockSize, c,  filterScale, filterMinArea, filterMaxArea, convertToNumber, resultKeysValues):

    global capaCrop
    global checkCapa
    global __resultsDirectory
    global __googleVisionDirectory

    # Read selected image
    img = cv2.imread(location)

    # Apply gray scale
    if len(img.shape) == 2:  # 灰度图
        gray_img = img
    elif len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Verify if need make blur
    if makeBlur:
        gray_img = cv2.GaussianBlur(gray_img, (1, 1), 2)
        thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,blockSize, c)
    else:
        thresh_img = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c)

    # cv2.imshow("tresh",thresh_img)
    # cv2.waitKey()

    # Create a vertical and horizontal copy based on trash image
    h_img = thresh_img.copy()
    v_img = thresh_img.copy()

    # ------------ Horizontal kernel and adjustments ------------

    # Get horizontal kernel size based on parameter of scale
    h_size = int(h_img.shape[1] / filterScale)

    # Retrieve all rects structuring based on hsize kernel and erode e dilate the result
    h_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (h_size,1))  
    h_erode_img = cv2.erode(h_img, h_structure, 1)
    h_dilate_img = cv2.dilate(h_erode_img, h_structure,5)


    # -----------------------------------------------------------
    
    # ------------ Vertical kernel and adjustments --------------

    # Get vertical kernel size based on parameter of scale
    v_size = int(v_img.shape[0] / filterScale)

    # Retrieve all rects structuring based on 1 x 13 kernel and erode e dilate the result
    v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
    v_erode_img = cv2.erode(v_img, v_structure, 1)
    v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

    cv2.imwrite("hdilate.jpg",h_dilate_img)
    cv2.imwrite("vdilate.jpg",v_dilate_img)

    # -----------------------------------------------------------


    # Crate a mask based on result of horizontal and vertical dilation and separate points by bitwise method
    mask_img = h_dilate_img + v_dilate_img
    joints_img = cv2.bitwise_and(h_dilate_img, v_dilate_img)

    # cv2.imshow("contours",joints_img)
    # cv2.waitKey(0)


    # Search all contours according mask
    contours, _ = cv2.findContours(mask_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Sort contours according orderMethod param
    (cntsSorted, boundingBoxes) = tools.sort_contours(contours, method=orderMethod)

    result = []
    cover = []
    resultContent =[]
    headerLineY = 0


    #first tables
    if index == -1:
        # --------- Iterate all rect contours and crop shapes ------
        for i in range(len(cntsSorted)):
            
            area = cv2.contourArea(cntsSorted[i])
            x, y, w, h = cv2.boundingRect(cntsSorted[i])

            # print(area)
            # print("x --> "+ str(x) + " y --> "+ str(y) + " w --> " + str(w) + " h --> "+str(h))

            if area > 1750 and area < 2000 and w > 900 and h > 15 and h < 20:
                headerLineY = y
                print("encontrou capa")

            if (area > filterMinArea and area < filterMaxArea):

                mask = np.zeros_like(img)
                # cv2.drawContours(mask, cnt, i, 255, -1)
                x, y, w, h = cv2.boundingRect(cntsSorted[i])
                crop = img[y:h + y, x:w + x]

                # cv2.imshow("crop",crop)
                # cv2.waitKey()

                # Encontrou a primeira tabela de dados químicos, antes disso, faz um crop para cima
                # para puxar os dados da análise
                if checkCapa == False and headerLineY != 0:
                    capaCrop = img[headerLineY:y , (x - 15):w + (x + 50)]
                    checkCapa = True
                    hash = random.getrandbits(128)
                    path = __resultsDirectory + "/cover" + str(i) + "_" + str(hash) + ".png"
                    cv2.imwrite(path, capaCrop)
                    cover.append(path)
                
                # crop = img[(y -15):h + (y + 5), (x - 15):w + (x + 50)]
                crop = img[y:h + y, x:w + x]
            
                hash = random.getrandbits(128)
                path = __resultsDirectory + "/table" + str(i) + "_" + str(hash) + ".png"
                cv2.imwrite(path, crop)


                if len(result) < 2:
                    result.append(path)

    else:

        # cv2.imshow("mask",mask_img)
        # cv2.waitKey()

        contoursh, _ = cv2.findContours(h_dilate_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        (cntsSorted, boundingBoxes) = tools.sort_contours(contoursh, method="bottom-to-top")

        x1, y1, w1, h1 = cv2.boundingRect(cntsSorted[1])
        x2, y2, w2, h2 = cv2.boundingRect(cntsSorted[0])

        cropH = y2 - y1
        cropW = w2 - x2

        # print(cropW)
        # print(cropH)
        # print(y1)

        clearImgTable = cv2.drawContours(gray_img, contours, -1, (255, 255, 255), 3)

        #create white image to set the crop
        hash = random.getrandbits(128)
        whitebg = 255 * np.ones(shape=[768, 1024, 3], dtype=np.uint8)
        pathBg = __resultsDirectory + "/whitebg.png"
        cv2.imwrite(pathBg,whitebg)
        path = __resultsDirectory + "/result_" + str(hash) + ".png"
        pathWhite = __resultsDirectory + "/resultwhite_" + str(hash) + ".png"

        cv2.imwrite(path, clearImgTable)

        # tools.textDeskew(path)

        # tools.levelTratment(path)

        tools.textCleaner(path,path)

        newimage = cv2.imread(path)

        h, w = clearImgTable.shape

        # cv2.imshow("clear aligned image",clearImgTable)
        # cv2.waitKey()

        print("crop y1 -> " +  str(y1) + " cropH -> "+ str(cropH) + "  x1 -> " + str(x1) + "  x2 -> " +str(x2) + " cropW -> "+ str(cropW))

        crop = clearImgTable[y1:y1 + cropH,0:x2 +cropW]

        height, width = crop.shape[:2]
        
        res = cv2.resize(crop,(4*width, 4*height), interpolation = cv2.INTER_CUBIC)
        

        
        cv2.imwrite(path, res)

        tools.textCleaner(path,path)
        tools.imagenegatetratment(path,path)
        tools.alphatratament(path, path)
        tools.removeBorder(path)


        # imgread = cv2.imread(path)

        # cv2.imshow("croped", imgread)
        # cv2.waitKey()

        # tools.setOnWhiteDocument(pathBg,path)

        resultContent.append(path)

        # copyfile(path, pathWhite)

        # tools.imagenegatetratment(path,path)

    # cv2.imshow("msdk",mask_img)
    # cv2.waitKey()

    
    # Found results, create a merge of all contents and detect table values with 
    # Machine Learning on Google Vision API
    
    if len(resultContent) > 0:
        extractValues = []
        if sequentialSend:
            extractValues = visionApi.sendSequentialGoogleVision(resultContent, numberSequentials)
        else:
            # fullPath = tools.merge_image(__googleVisionDirectory,resultContent,0,2,'white',False,"tabela"+str(index))
            # tools.textCleaner(fullPath,fullPath)
            
            extractValues = tesseract.readImage(resultContent[0])

            # print("RetornoTesseract", extractValues)

            # extractValues, confidence = visionApi.sendToGoogleVision(resultContent[0],None,convertToNumber)

            # resultKeysValues['Confidencia'] += confidence

            if len(extractValues) == 0:
                raise Exception('Não foi possível retornar os valore: '+ extractValues)

        for idx,value in enumerate(extractValues):
            setValue = value         
            if index == 0:

                if idx == 0:
                    resultKeysValues['dadosExtraidos']['amostra'] = setValue if setValue else "N.D"
                if idx == 1:
                    resultKeysValues['dadosExtraidos']['area_ha'] = setValue if setValue else "N.D"
                if idx == 2:
                    resultKeysValues['dadosExtraidos']['argila'] = setValue if setValue else "N.D"
                if idx == 3:
                    resultKeysValues['dadosExtraidos']['classe_textural'] = setValue if setValue else "N.D"
                if idx == 4:
                    resultKeysValues['dadosExtraidos']['ph_H20'] = setValue if setValue else "N.D"
                if idx == 5:
                    resultKeysValues['dadosExtraidos']['indice_SMP'] = setValue if setValue else "N.D"
                if idx == 6:
                    resultKeysValues['dadosExtraidos']['m_o'] = setValue if setValue else "N.D"
                if idx == 7:
                    resultKeysValues['dadosExtraidos']['p'] = setValue if setValue else "N.D"
                if idx == 8:
                    resultKeysValues['dadosExtraidos']['k'] = setValue if setValue else "N.D"
                if idx == 9:
                    resultKeysValues['dadosExtraidos']['ca'] = setValue if setValue else "N.D"
                if idx == 10:
                    resultKeysValues['dadosExtraidos']['mg'] = setValue if setValue else "N.D"
                if idx == 11:
                    resultKeysValues['dadosExtraidos']['al'] = setValue if setValue else "N.D"
                if idx == 12:                    
                    resultKeysValues['dadosExtraidos']['h_al'] = setValue if setValue else "N.D"
            else:

                if idx == 1:
                    resultKeysValues['dadosExtraidos']['ctc_efetiva'] = setValue if setValue else "N.D"
                if idx == 2:
                    resultKeysValues['dadosExtraidos']['ctc_ph'] = setValue if setValue else "N.D"
                if idx == 3:
                    resultKeysValues['dadosExtraidos']['saturacao_bases'] = setValue if setValue else "N.D"
                if idx == 4:
                    resultKeysValues['dadosExtraidos']['saturacao_al'] = setValue if setValue else "N.D"
                if idx == 5:
                    resultKeysValues['dadosExtraidos']['s'] = setValue if setValue else "N.D"
                if idx == 6:
                    resultKeysValues['dadosExtraidos']['b'] = setValue if setValue else "N.D"
                if idx == 7:
                    resultKeysValues['dadosExtraidos']['cu'] = setValue if setValue else "N.D"
                if idx == 8:
                    resultKeysValues['dadosExtraidos']['zn'] = setValue if setValue else "N.D"
                if idx == 9:
                    resultKeysValues['dadosExtraidos']['mn'] = setValue if setValue else "N.D"
                if idx == 10:
                    resultKeysValues['dadosExtraidos']['mo'] = setValue if setValue else "N.D"
                if idx == 11:
                    resultKeysValues['dadosExtraidos']['fe'] = setValue if setValue else "N.D"
                if idx == 12:
                    resultKeysValues['dadosExtraidos']['na'] = setValue if setValue else "N.D"
          
    processResult = ProcessResult()
    processResult.tables = result
    processResult.cover = cover
    processResult.content = resultKeysValues

    return processResult

def processImage(analises, mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file):

    #Carrega o json do layout
    keysResultValuesJson = {}
    try:
        with open(parm_layout_file) as json_file:  
            keysResultValuesJson = json.load(json_file)
    except:
        print("Houve uma falha ao ler o layout")
        exit(0)

    if file.endswith(".pdf"):
        file = "imagemConvertida.png"
        tools.pdfToImage(parm_input_folder_images + "/" + file,parm_input_folder_images + "/" + file)
        print("# Converteu" + file + " para imagem")

    try:
        hash = random.getrandbits(128)
        output_file = tools.initial_tratment(parm_input_folder_images + file, __dirpath + "/resultAdjust.jpg")
    
        result = ReadAdjustImage(-1,output_file,useSequentialSend,numberPerRequest,"top-to-bottom",False,15,-1,mainTablesScale,startMainTableInterval,endMainTableInterval,parm_convert_number,{})

        if parm_extract_method == 'full':
            for cover in result.cover:
                tools.extractCover(cover, keysResultValuesJson)

        if len(result.tables) >= 2:

            for idx, r in enumerate(result.tables):
                if idx == 0:
                    # tools.textCleaner(r,r)
                    rs = ReadAdjustImage(idx,r,useSequentialSend,numberPerRequest,"left-to-right",True, 15, -1, secondaryTableScale, startSecondTableInterval, endSecondTableInterval, parm_convert_number, keysResultValuesJson)
                    keysResultValuesJson = rs.content

                if idx == 1 and parm_extract_method == 'default' or parm_extract_method == 'full':
                    # tools.textCleaner(r,r)
                    rs = ReadAdjustImage(idx,r,useSequentialSend,numberPerRequest,"left-to-right",True, 15, -1, secondaryTableScale, startSecondTableInterval, endSecondTableInterval, parm_convert_number,  keysResultValuesJson)
                    keysResultValuesJson = rs.content

            keysResultValuesJson["Confidencia"] = keysResultValuesJson["Confidencia"]/2
            keysResultValuesJson["FilePath"] = __successDirectory + "/" +  file

            analises.append(keysResultValuesJson)

            move(parm_input_folder_images + file, __successDirectory + "/" +  file)
        
        else:
            move(parm_input_folder_images + file, __errorDirectory + "/" +  file)

    except Exception as e:
        print("Arquivo com problema " +  parm_input_folder_images + file + ". Erro: " + str(e))
        move(parm_input_folder_images + file, __errorDirectory + "/" +  file)
        
    with open(parm_output_results + "resultados.json", 'w', encoding='utf8') as json_file:
        json.dump(analises, json_file, ensure_ascii=False)

    tools.create_csv(analises, parm_output_results + "resultados.csv")

    # tools.removeTemporaryFiles(__resultsDirectory)

    return analises

def execute(parm_input_folder_images = '', parm_layout_file = '', parm_extract_method = 'default', parm_output_results = "", parm_convert_number = True):

    global checkCapa
    global capaCrop
    global __resultsDirectory
    global __dirpath

    
    mainTablesScale = 30
    secondaryTableScale = 17
    useSequentialSend = False
    numberPerRequest  = 5 #If useSequentialSend = True
    # startMainTableInterval = 65000
    # endMainTableInterval = 120000
    startMainTableInterval = 17000
    endMainTableInterval = 80000
    startSecondTableInterval = 1600
    endSecondTableInterval = 2400
  
    
    # #Params
    # parm_input_folder_images = ''
    # parm_layout_file = '' #fields layout
    # parm_extract_method = 'default' # simple, default, full
    # parm_output_results = ""
    # parm_convert_number = True

    

    # try:
    #     parm_input_folder_images = sys.argv[1]
    #     parm_layout_file = sys.argv[2]
    #     parm_extract_method = sys.argv[3]
    #     parm_output_results = sys.argv[4]
    #     parm_convert_number = sys.argv[5]
    # except:
    if parm_input_folder_images != '' and parm_layout_file != '':
        print("Nem todos os parametros foram informados, utilizando defaults")
    else:
        print("Informe o diretório para ler as imagens por parametro")
        exit(0)

    analises = []

    # Roda todos os arquivos do diretório
    for (directory, dirnames, filenames) in walk(parm_input_folder_images):
           
        #Cria diretorio que será usado para guardar as imagens temporárias
        if not os.path.exists(__resultsDirectory):
            os.makedirs(__resultsDirectory)

        #Cria diretorio que será usado para guardar as imagens com sucesso
        if not os.path.exists(__successDirectory):
            os.makedirs(__successDirectory)

        #Cria diretorio que será usado para guardar as imagens com erro
        if not os.path.exists(__errorDirectory):
            os.makedirs(__errorDirectory)

        

        if len(filenames) > 0:
            analises = []
            threads = []

            for file in filenames:
                analises = processImage(analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file)
                # t =  threading.Thread(target=processImage, args=(analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file))
                # t.start()
                # threads.append(t)
                # time.sleep(60)
                # _thread.start_new_thread(processImage, (analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file))


            # print ("Total threads running ", len(threads))
            # # Wait for all threads to complete
            # for t in threads:
            #     t.join()
                
        else:
            print("Nenhum arquivo encontrado no diretório")

    return json.dumps(analises)

def main():

    global checkCapa
    global capaCrop
    global __resultsDirectory
    global __dirpath

    
    mainTablesScale = 30
    secondaryTableScale = 17
    useSequentialSend = False
    numberPerRequest  = 5 #If useSequentialSend = True
    # startMainTableInterval = 65000
    # endMainTableInterval = 120000
    startMainTableInterval = 17000
    endMainTableInterval = 80000
    startSecondTableInterval = 1600
    endSecondTableInterval = 2400
  
    
    #Params
    parm_input_folder_images = ''
    parm_layout_file = '' #fields layout
    parm_extract_method = 'default' # simple, default, full
    parm_output_results = ""
    parm_convert_number = True

    

    try:
        parm_input_folder_images = sys.argv[1]
        parm_layout_file = sys.argv[2]
        parm_extract_method = sys.argv[3]
        parm_output_results = sys.argv[4]
        parm_convert_number = sys.argv[5]
    except:
        if parm_input_folder_images != '' and parm_layout_file != '':
            print("Nem todos os parametros foram informados, utilizando defaults")
        else:
            print("Informe o diretório para ler as imagens por parametro")
            exit(0)

    # Roda todos os arquivos do diretório
    for (directory, dirnames, filenames) in walk(parm_input_folder_images):
           
        #Cria diretorio que será usado para guardar as imagens temporárias
        if not os.path.exists(__resultsDirectory):
            os.makedirs(__resultsDirectory)

        #Cria diretorio que será usado para guardar as imagens com sucesso
        if not os.path.exists(__successDirectory):
            os.makedirs(__successDirectory)

        #Cria diretorio que será usado para guardar as imagens com erro
        if not os.path.exists(__errorDirectory):
            os.makedirs(__errorDirectory)

        

        if len(filenames) > 0:
            analises = []
            threads = []

            for file in filenames:
                processImage(analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file)
                # t =  threading.Thread(target=processImage, args=(analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file))
                # t.start()
                # threads.append(t)
                # time.sleep(60)
                # _thread.start_new_thread(processImage, (analises,mainTablesScale, secondaryTableScale, useSequentialSend, numberPerRequest, startMainTableInterval, endMainTableInterval, startSecondTableInterval, endSecondTableInterval, parm_input_folder_images, parm_layout_file, parm_extract_method, parm_output_results, parm_convert_number, file))


            # print ("Total threads running ", len(threads))
            # # Wait for all threads to complete
            # for t in threads:
            #     t.join()
                
        else:
            print("Nenhum arquivo encontrado no diretório")


if __name__ == "__main__": main()

