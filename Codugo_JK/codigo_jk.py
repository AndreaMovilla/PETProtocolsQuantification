import numpy as np
import matplotlib
from numpy.core.fromnumeric import shape
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import nrrd
import napari
import cv2
from skimage.segmentation import active_contour
from os import walk
from os.path import splitext
from os.path import join
from functions import *
import pandas as pd
import xlsxwriter

main_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_JK/M04_Static/CT' #Directorio a la carpeta principal
excelname='staticcontrast.xlsx' #Nombre del documento.xlsx de salida
direct = directories(main_path + '/FDG_segmentations')  #Directorio de las segmentaciones de actividad
segFDG = importnrrd(main_path + '/FDG_segmentations') #Segmentaciones de actividad
segBG=importnrrd(main_path + '/BG_segmentations') #Segmentaciones de fondo sin actividad
images=importnrrd(main_path + '/CT') #Imágenes a analizar
pets=names(main_path + '/CT') #Nombre de archivo de la imagen a analizar

#Obtenemos segmentacionesen 3 planos
segBGtotal=[]
for i in range(0,len(segBG)):
      segplanosBG=repeatseg(segBG[i])
      segBGtotal.append(segplanosBG)
segFDGtotal = []
for i in range(0, len(segFDG)):
   segplanosFDG = repeatseg(segFDG[i])
   segFDGtotal.append(segplanosFDG)

#Pasamos segmetaciones a bool
segBGbool=[]
for i in range(0,len(segBGtotal)):
   segBGbool.append(segBGtotal[i].astype('bool'))

segFDGbool=[]
for i in range(0,len(segFDGtotal)):
   segFDGbool.append(segFDGtotal[i].astype('bool'))

#Calculamos el contraste por sectores

dic={}
dic['Names']=direct
for j in range(0,len(images)):
    Contrasttotal=[]
    for i in range(0,len(segBGbool)):
        imagensegBG=np.copy(images[j])
        imagensegFDG = np.copy(images[j])
        imagensegBG[~segBGbool[i]]=np.nan
        imagensegFDG[~segFDGbool[i]] = np.nan
        intensidadBG=np.nanmean(imagensegBG)
        intensidadFDG =np.nanmean(imagensegFDG)
        contrast=intensidadFDG/intensidadBG
        Contrasttotal.append(contrast)
    dic[pets[j]]=Contrasttotal


#Guardamos valores del contraste en un xlsx
keylist=dic.keys()
valuelist=dic.values()
df = pd.DataFrame(data=dic)
df = (df.T)
df.to_excel(excelname)