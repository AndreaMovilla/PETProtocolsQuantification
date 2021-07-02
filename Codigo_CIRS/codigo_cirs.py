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

main_path= '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/PET_analisis' #Directorio a la carpeta principal
main_path_ref = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/M04_Static' #Directorio a la carpeta de referencia
excelname='M01_sin1_RC2.xlsx' #Nombre del documento.xlsx de salida

direct = directories(main_path + '/Reference_segmentations2') # Directorio de las segmentaciones de las imágenes a analizar
seg = importnrrd(main_path + '/Reference_segmentations2') #Segmentaciones de las imágenes a analizar
segref=importnrrd(main_path_ref + '/Reference_segmentations') #Segmentaciones de la imagen de referencia
direct_segref=directories(main_path_ref + '/Reference_segmentations') #Segmentaciones de la imagen de referencia
imageref=nrrd.read(main_path_ref + '/PET/PET_Static.nrrd')[0] #Imagen de referencia
images = importnrrd(main_path + '/PET') #Imágenes a analizar
pets=names(main_path + '/PET') #Nombre de archivo de cada imagen a analizar

#Obtenemos segmentaciones para los dos tipos de imágenes
segmentacionesrefbool=[]
for i in range(0,len(segref)):
   segmentacionesrefbool.append(segref[i].astype('bool'))

segmentacionesbool=[]
for i in range(0,len(seg)):
   segmentacionesbool.append(seg[i].astype('bool'))


#Obtenemos intensidad para cada segmentación en la imagen de referencia
intensidadesref=[]
for i in range(0,len(segref)):
        imagensegmentadaref=np.copy(imageref)
        imagensegmentadaref[~segmentacionesrefbool[i]]=np.nan
        intensidadref=np.nanmean(imagensegmentadaref)
        intensidadesref.append(intensidadref)


#Realizamos todas las segmentaciones en las imágenes para 1 movimiento. Calculamos RC
dic={}
dic['Names']=direct
intensidades_total=[]
for j in range(0,len(images)):
    RCtotal=[]
    intensidadseg = []
    for i in range(0,len(seg)):
        imagensegmentada=np.copy(images[j])
        imagensegmentada[~segmentacionesbool[i]]=np.nan
        intensidad=np.nanmean(imagensegmentada)
        intensidadseg.append(intensidad)
        RC=intensidad/intensidadesref[i]
        RCtotal.append(RC)
    intensidades_total.append(intensidadseg)
    dic[pets[j]]=RCtotal


#Guardamos valores de RC en un .xlsx
keylist=dic.keys()
valuelist=dic.values()
df = pd.DataFrame(data=dic)
df = (df.T)
df.to_excel(excelname)




