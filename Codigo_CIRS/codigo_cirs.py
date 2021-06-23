import numpy as np
import matplotlib
from numpy.core.fromnumeric import shape
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import nrrd
import cv2
from os import walk
from os.path import splitext
from os.path import join
from functions import *
import pandas as pd
import csv

main_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M01_Sin1/Prosp' #Directorio a la carpeta principal
main_path_ref = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M01_Sin1/Prosp' #Directorio a la carpeta de referencia
excelname='staticvolumes.xlsx' #Nombre del documento.xlsx de salida
direct = directories(main_path + '/Reference_segmentations')  # Directorio de las segmentaciones de las imágenes a analizar
seg = importnrrd(main_path + '/Reference_segmentations') #Segmentaciones de las imágenes a analizar
segref=importnrrd(main_path_ref + '/Reference_segmentations') #Segmentaciones de la imagen de referencia
imageref=nrrd.read(main_path_ref + '/PET')[0] #Imagen de referencia
images = importnrrd(main_path + '/PET') #Imágenes a analizar
pets=names(main_path + '/PET') #Nombre de archivo de cada imagen a analizar

#Obtenemos segmentaciones para los dos tipos de imágenes
segmentacionesrefbool=[]
for i in range(0,len(seg)):
   segmentacionesrefbool.append(segref[i].astype('bool'))

segmentacionesbool=[]
for i in range(0,len(seg)):
   segmentacionesbool.append(seg[i].astype('bool'))


#Obtenemos intensidad para cada segmentación en la imagen de referencia
intensidadesref=[]
for i in range(0,len(seg)):
        imagensegmentadaref=np.copy(imageref[0])
        imagensegmentadaref[~segmentacionesrefbool[i]]=np.nan
        intensidadref=np.nanmean(imagensegmentadaref)
        intensidadesref.append(intensidadref)


#Realizamos todas las segmentaciones en las imágenes para 1 movimiento. Calculamos RC
dic={}
dic['Names']=direct
for j in range(0,len(images)):
    RCtotal=[]
    for i in range(0,len(seg)):
        imagensegmentada=np.copy(images[j])
        imagensegmentada[~segmentacionesbool[i]]=np.nan
        intensidad=np.nanmean(imagensegmentada)
        RC=intensidad/intensidadesref[i]
        RCtotal.append(RC)
    dic[pets[j]]=RCtotal


#Guardamos valores de RC en un .csv
keylist=dic.keys()
valuelist=dic.values()
df = pd.DataFrame(data=dic)
df = (df.T)
df.to_excel(excelname)




