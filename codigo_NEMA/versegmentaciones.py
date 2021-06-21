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

direct = directories(main_path + '/TS_segmentations')  # Directorio de las segmentaciones
seg = importnrrd(main_path + '/TS_segmentations')  # Importamos segmentaciones de referencia
image = nrrd.read(main_path + '/PET/NEMA_staticRes.nrrd')[0] # El que va bien



viewer = napari.Viewer()
napar_img = viewer.add_image(image,name='PetScan',gamma=0.62)
napar_seg0 = viewer.add_image(seg[0])
napar_seg1 = viewer.add_image(seg[1])
napar_seg2 = viewer.add_image(seg[2])
napar_seg3 = viewer.add_image(seg[3])
napar_seg4 = viewer.add_image(seg[4])
