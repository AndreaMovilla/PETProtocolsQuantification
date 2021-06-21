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

main_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M04_Static/Static'
excelname='staticvolumes.xlsx'
direct = directories(main_path + '/Reference_segmentations') # Directorio de las segmentaciones
seg = importnrrd(main_path + '/Reference_segmentations')  # Importamos segmentaciones de referencia
images = importnrrd(main_path + '/PET') # El que va bien
pets=names(main_path + '/PET') # Nombre de archivo de cada imagen PET
voxeldim =4# tamaño de los voxeles, en mm

#Calculamos el volumen con Threshold segmentation y escribimos los valores en un diccionario
dic = {}
dic['Names'] = direct
for j in range(0, len(pets)): #TODO: cambiado len(images) a len(pets) para no liarla con el numero de imgs
	volumenes = []
	coordenadas = []
	for i in range(0, len(seg)):
		volumen = thresholdseg(seg[i], images[j], voxeldim)
		filename='TS_'+direct[i]+'_'+pets[j]
		nrrd.write(filename, volumen[1])
		volumenes.append(volumen[0])
	dic[pets[j]] = volumenes



# Guardamos valores del volumen en un .xlxs
keylist = dic.keys()
valuelist = dic.values()

df = pd.DataFrame(data=dic)
df = (df.T)
df.to_excel(excelname)



