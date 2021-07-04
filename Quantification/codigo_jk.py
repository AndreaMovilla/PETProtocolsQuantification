import numpy as np
import matplotlib
from numpy.core.fromnumeric import shape
matplotlib.use('Qt5Agg')
import nrrd
import cv2
from os import walk
from os.path import splitext
from os.path import join
from functions import *
import pandas as pd
import xlsxwriter

main_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_JK/PET_analisis' #Directorio a la carpeta principal
main_path_ref = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_JK/M04_Static/PET' #Directorio a la carpeta de referencia
excelname='MO1_sin1_contrastprueba1.xlsx' #Nombre del documento.xlsx de salida
ad_time=[58639,57883] #Hora de estudio estático y estudio dinámico, en segundos
half_life=109.771*60 #Periodo de semidesintegración del radiotrzador, en segundos
time=ad_time[0]-ad_time[1] #Tiempo entre estudios

direct = directories(main_path + '/FDG_segmentations2')  #Directorio de las segmentaciones de actividad
segFDG = importnrrd(main_path + '/FDG_segmentations2') #Segmentaciones de actividad
segBG=importnrrd(main_path + '/BG_segmentations2') #Segmentaciones de fondo sin actividad
segrefFDG=importnrrd(main_path_ref + '/FDG_segmentations') #Segmentaciones de actividad de la imagen de referencia
segrefBG=importnrrd(main_path_ref + '/BG_segmentations') #Segmentaciones de fondo sin actividad de la imagen de referencia
imageref=importnrrd(main_path_ref + '/PET')#Imagen de referencia
images=importnrrd(main_path + '/PET') #Imágenes a analizar
pets=names(main_path + '/PET') #Nombre de archivo de la imagen a analizar


#Obtenemos las segmentaciones de la imagen de referencia y sus contrastes
segrefBGtotal = []
for i in range(0, len(segrefBG)):
    segplanosrefBG = repeatseg(segrefBG[i])
    segrefBGtotal.append(segplanosrefBG)
segrefFDGtotal = []
for i in range(0, len(segrefFDG)):
    segplanosrefFDG = repeatseg(segrefFDG[i])
    segrefFDGtotal.append(segplanosrefFDG)

#Pasamos segmetaciones a bool
segrefBGbool=[]
for i in range(0,len(segrefBGtotal)):
   segrefBGbool.append(segrefBGtotal[i].astype('bool'))


segrefFDGbool=[]
for i in range(0,len(segrefFDGtotal)):
   segrefFDGbool.append(segrefFDGtotal[i].astype('bool'))

dicref = {}
dicref['Names'] = direct
Contrastreftotal=[]
BGreftotal=[]
FDGreftotal=[]
for i in range(0,len(segrefBGbool)):
    imagensegrefBG=np.copy(imageref[0])
    imagensegrefFDG = np.copy(imageref[0])
    imagensegrefBG[~segrefBGbool[i]]=np.nan
    imagensegrefFDG[~segrefFDGbool[i]] = np.nan
    intensidadrefBG=np.nanmean(imagensegrefBG)
    intensidadrefFDG =np.nanmean(imagensegrefFDG)
    contrastref=intensidadrefFDG/intensidadrefBG
    Contrastreftotal.append(contrastref)
    FDGreftotal.append(intensidadrefFDG)
    BGreftotal.append(intensidadrefBG)
dicref['Estático'] = Contrastreftotal
dicref['Estático BG'] =BGreftotal
dicref['Estático FDG'] =FDGreftotal

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
dic2 = {}
dic2['Names'] = direct
dicBG = {}
dicBG['Names'] = direct
dicFDG = {}
dicFDG['Names'] = direct
for j in range(0,len(images)):
    Contrasttotal=[]
    RCtotal = []
    FDGtotal = []
    BGtotal = []
    for i in range(0,len(segBGbool)):
        imagensegBG=np.copy(images[j])
        imagensegFDG = np.copy(images[j])
        imagensegBG[~segBGbool[i]]=np.nan
        imagensegFDG[~segFDGbool[i]] = np.nan
        intensidadBG=np.nanmean(imagensegBG)*np.exp(-np.log(2)*time/half_life)
        intensidadFDG =np.nanmean(imagensegFDG)*np.exp(-np.log(2)*time/half_life)
        contrast=intensidadFDG/intensidadBG
        RC=contrast/Contrastreftotal[i]
        RCtotal.append(RC)
        Contrasttotal.append(contrast)
        FDGtotal.append(intensidadFDG)
        BGtotal.append(intensidadBG)
    dic[pets[j]]=Contrasttotal
    dic2[pets[j]]=RCtotal
    dicBG[pets[j]] = BGtotal
    dicFDG[pets[j]] = FDGtotal

#Guardamos valores del contraste en un xlsx
writer = pd.ExcelWriter(excelname)
dfref = pd.DataFrame(data=dicref)
dfref = (dfref.T)
dfref.to_excel(writer, sheet_name="Estático")


df1 = pd.DataFrame(data=dic)
df1 = (df1.T)
df1.to_excel(writer, sheet_name="Contrastes")


df2 = pd.DataFrame(data=dic2)
df2 = (df2.T)
df2.to_excel(writer, sheet_name="CR")


df3 = pd.DataFrame(data=dicBG)
df3 = (df3.T)
df3.to_excel(writer, sheet_name="Concentracion BG")


df4 = pd.DataFrame(data=dicFDG)
df4 = (df4.T)
df4.to_excel(writer, sheet_name="Concentracion FDG")
writer.save()