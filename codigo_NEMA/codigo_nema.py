import numpy as np
import matplotlib
from numpy.core.fromnumeric import shape
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import nrrd
import cv2
from os import walk
from os.path import splitext
from os.path import join
from functions import *
import pandas as pd
import xlsxwriter

main_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/PET_analisis'
main_path_ref = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M04_Static/Static' #Directorio a la carpeta de referencia
excelname='M01_sin1volumes.xlsx'
direct = directories(main_path + '/Reference_segmentations') # Directorio de las segmentaciones
seg = importnrrd(main_path + '/Reference_segmentations')  # Importamos segmentaciones de referencia
segref=importnrrd(main_path_ref + '/Reference_segmentations') #Segmentaciones de la imagen de referencia
imageref=nrrd.read(main_path_ref + '/PET/PET_Static.nrrd')[0] #Imagen de referencia
images = importnrrd(main_path + '/PET') # El que va bien
pets=names(main_path + '/PET') # Nombre de archivo de cada imagen PET
voxeldim =4# tamaño de los voxeles, en mm
voxeldimref =2# tamaño de los voxeles de la imagen de referencia, en mm

#Calculamos el volumen  de la imagen de referencia con Threshold segmentation
volumenesref = []

dicref = {}
dicref['Names'] = direct
for i in range(0, len(seg)):
	volumenref = thresholdseg(segref[i], imageref, voxeldimref)
	filename = 'TS_' + direct[i] + '_' + 'static.nrrd'
	nrrd.write(filename, volumenref[1])
	volumenesref.append(volumenref[0])
dicref['Estático'] = volumenesref



#Calculamos el volumen  y el CR con Threshold segmentation y escribimos los valores en dos diccionarios
dic = {}
dic['Names'] = direct
dic2 = {}
dic2['Names'] = direct
for j in range(0, len(pets)):
	volumenes = []
	coordenadas = []
	RCtotal=[]
	for i in range(0, len(seg)):
		volumen = thresholdseg(seg[i], images[j], voxeldim)
		filename='TS_'+direct[i]+'_'+pets[j]
		nrrd.write(filename, volumen[1])
		RC=volumen[0]/volumenesref[i]
		RCtotal.append(RC)
		volumenes.append(volumen[0])
	dic[pets[j]] = volumenes
	dic2[pets[j]] = RCtotal



# Guardamos valores del volumen y CR en un .xlxs
writer = pd.ExcelWriter(excelname)
dfref = pd.DataFrame(data=dicref)
dfref = (dfref.T)
dfref.to_excel(writer, sheet_name="Vol. estático")


df1 = pd.DataFrame(data=dic)
df1 = (df1.T)
df1.to_excel(writer, sheet_name="Volúmenes")


df2 = pd.DataFrame(data=dic2)
df2 = (df2.T)
df2.to_excel(writer, sheet_name="CR")
writer.save()



