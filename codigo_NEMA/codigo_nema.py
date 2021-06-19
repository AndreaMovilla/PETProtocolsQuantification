import numpy as np
import matplotlib
from numpy.core.fromnumeric import shape

matplotlib.use('TkAgg')
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
import csv

main_path = '/Users/veromieites/Desktop/MoviTFM'

direct = directories(main_path + '/NewData_4DDynamic/Segmentations')  # Directorio de las segmentaciones
seg = importnrrd(main_path + '/NewData_4DDynamic/Segmentations')  # Importamos segmentaciones de referencia
images = nrrd.read(main_path + '/NewData_4DDynamic/NEMA_Exhal40%.nrrd')[0] # El que va bien
pets = names(main_path + '/NewData_4DDynamic/')  # Nombre de archivo de cada imagen PET
pets = [pet for pet in pets if not pet.startswith('S')]
'''direct = directories(main_path + '/Reference_3DStatic/NEMA_Static.nrrd')  # Directorio de las segmentaciones
seg = importnrrd(main_path + '/Reference_3DStatic/NEMA_Static.nrrd')  # Importamos segmentaciones de referencia
images = nrrd.read(main_path + '/Reference_3DStatic/NEMA_Static.nrrd')[0]  # El que va mal
pets = names(main_path + '/Reference_3DStatic/NEMA_Static.nrrd')  # Nombre de archivo de cada imagen PET'''

voxeldim = 4  # tamaño de los voxeles, en mm

# Calculamos el volumen con Threshold segmentation y escribimos los valores en un diccionario
dic = {}
dic['Names'] = direct
for j in range(0, len(pets)): #TODO: cambiado len(images) a len(pets) para no liarla con el numero de imgs
	volumenes = []
	coordenadas = []
	for i in range(0, len(seg)):
		volumen = thresholdseg(seg[i], images, voxeldim)
		volumenes.append(volumen)
	dic[pets[j]] = volumenes

# for j in range(0,len(images)):
#     volumenes=[]
#     for i in range(0,len(seg)):
#         imagensegmentadaref=np.copy(images(i))
#         imagensegmentadaref[~images(i)[]]=np.nan


# Guardamos valores del volumen en un .csv
keylist = dic.keys()
valuelist = dic.values()
with open('M01_prosp.csv', 'w') as f:
	for key in dic.keys():
		# key.replace("[","")
		f.write("%s,%s\n" % (key, dic[key]))
