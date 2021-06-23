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


seg_path = '/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M01_Sin1/Prosp/Reference_segmentations'
image_path='/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_NEMA/M01_Sin1/Prosp/PET/M01_Asc/PET/70Asc9040PETRetrospective.nrrd'
direct = directories(seg_path )  #Directorio de las segmentaciones
seg = importnrrd(seg_path)  #Importamos segmentaciones
image = nrrd.read(image_path)[0] #Importamos imagen



viewer = napari.Viewer()
napar_img = viewer.add_image(image,name='PetScan',gamma=0.62, colormap='twilight')
for i in range(0, len(seg)):
    napar_seg = viewer.add_image(seg[i],name=direct[i], colormap='red',blending='additive',opacity=0.4)



#NAPAR_SEG1 = VIEWER.ADD_IMAGE(SEG[1], COLORMAP='RED',BLENDING='ADDITIVE',OPACITY=0.4)
#NAPAR_SEG2 = VIEWER.ADD_IMAGE(SEG[2], COLORMAP='RED',BLENDING='ADDITIVE',OPACITY=0.4)
#NAPAR_SEG3 = VIEWER.ADD_IMAGE(SEG[3], COLORMAP='RED',BLENDING='ADDITIVE',OPACITY=0.4)
#NAPAR_SEG4 = VIEWER.ADD_IMAGE(SEG[4], COLORMAP='RED',BLENDING='ADDITIVE',OPACITY=0.4)
