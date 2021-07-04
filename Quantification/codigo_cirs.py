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
excelname='M01_sin1_RCprueba1.xlsx' #Nombre del documento.xlsx de salida
ad_time=[60345,57258] #Hora de estudio estático y estudio dinámico, en segundos
half_life=109.771*60 #Periodo de semidesintegración del radiotrzador, en segundos
time=ad_time[0]-ad_time[1] #Tiempo entre estudios
#importamos
direct = directories(main_path + '/Reference_segmentations') # Directorio de las segmentaciones de las imágenes a analizar
seg = importnrrd(main_path + '/Reference_segmentations') #Segmentaciones de las imágenes a analizar
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
dic_ref={}
dic_ref['Names']=direct
for i in range(0,len(segref)):
        imagensegmentadaref=np.copy(imageref)
        imagensegmentadaref[~segmentacionesrefbool[i]]=np.nan
        intensidadref=np.nanmean(imagensegmentadaref)
        intensidadesref.append(intensidadref)
dic_ref['Estático']=intensidadesref

#Realizamos todas las segmentaciones en las imágenes para 1 movimiento. Calculamos RC
dic={}
dic['Names']=direct
dic2={}
dic2['Names']=direct
intensidades_total=[]
for j in range(0,len(images)):
    RCtotal=[]
    intensidadseg = []
    for i in range(0,len(seg)):
        imagensegmentada=np.copy(images[j])
        imagensegmentada[~segmentacionesbool[i]]=np.nan
        intensidad=np.nanmean(imagensegmentada)*np.exp(-np.log(2)*time/half_life)
        intensidadseg.append(intensidad)
        RC=intensidad/intensidadesref[i]
        RCtotal.append(RC)
    intensidades_total.append(intensidadseg)
    dic2[pets[j]]=intensidadseg
    dic[pets[j]]=RCtotal


#Guardamos valores de RC en un .xlsx
writer = pd.ExcelWriter(excelname)
dfref = pd.DataFrame(data=dic_ref)
dfref =(dfref.T)
dfref.to_excel(writer, sheet_name="Intensidad estático")

df2 = pd.DataFrame(data=dic2)
df2 =(df2.T)
df2.to_excel(writer, sheet_name="Intensidades")

df = pd.DataFrame(data=dic)
df =(df.T)
df.to_excel(writer, sheet_name="RC")
writer.save()



