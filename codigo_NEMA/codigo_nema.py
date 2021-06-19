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
import csv

main_path = '/Users/veromieites/Desktop/MoviTFM'

direct = directories(main_path + '/NewData_4DDynamic/Segmentations')  # Directorio de las segmentaciones
seg = importnrrd(main_path + '/NewData_4DDynamic/Segmentations')  # Importamos segmentaciones de referencia
#images = nrrd.read(main_path + '/NewData_4DDynamic/NEMA_Exhal40%.nrrd')[0] # El que va bien
#pets = names(main_path + '/NewData_4DDynamic/')  # Nombre de archivo de cada imagen PET


#direct = directories(main_path + '/Reference_3DStatic/Segmentations')  # Directorio de las segmentaciones
#seg = importnrrd(main_path + '/Reference_3DStatic/Segmentations')  # Importamos segmentaciones de referencia
#images = nrrd.read(main_path + '/Reference_3DStatic/NEMA_Static.nrrd')[0]  # El que tambien va bien
pets = names(main_path + '/Reference_3DStatic/')  # Nombre de archivo de cada imagen PET

pets = [pet for pet in pets if not pet.startswith('S')] # Elimina las segmentaciones y deja los pets

images = nrrd.read(main_path + '/Reference_3DStatic/PETStaticprueba2.nrrd')[0]  # El 3D con las dims del 4D
pets = pets[1] # el nombre asociado


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


viewer = napari.Viewer()
napar_img = viewer.add_image(images,name='PetScan',gamma=0.62)
napar_seg0 = viewer.add_image(seg[0],name='seg 26',colormap='cyan',blending='additive',opacity=0.5,contrast_limits=[-2.04, 8.415000000000003])
napar_seg1 = viewer.add_image(seg[1],name='seg 11',colormap='green',blending='additive',opacity=0.5,contrast_limits=[-2.04, 8.415000000000003])
napar_seg2 = viewer.add_image(seg[2],name='seg 03',colormap='PiYG',blending='additive',opacity=0.5,contrast_limits=[-2.04, 8.415000000000003])

napar_seg0.contrast_limits = [-2.04, 8.415000000000003]
napar_seg1.contrast_limits = [-2.04, 8.415000000000003]
napar_seg2.contrast_limits = [-2.04, 8.415000000000003]

