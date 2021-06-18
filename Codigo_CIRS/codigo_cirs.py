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


direct=directories('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/segmentaciones')
seg=importnrrd('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/segmentaciones')
segref=importnrrd('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/M04_Static/SEGREFERENCIA2')
imageref=importnrrd('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/M04_Static/PET')
images=importnrrd('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/M02_Typ7/Prosp_PET')
pets=names('/Users/andreamovilla/Desktop/TFM_Respiratory_NRRD/D01_CIRS/M02_Typ7/Prosp_PET')

#realizamos segmentaciones de referencia
segmentacionesrefbool=[]
for i in range(0,len(seg)):
   segmentacionesrefbool.append(segref[i].astype('bool'))

segmentacionesbool=[]
for i in range(0,len(seg)):
   segmentacionesbool.append(seg[i].astype('bool'))


#Obtenemos intensidad para cada regmentación en la imagen estática
intensidadesref=[]
for i in range(0,len(seg)):
        imagensegmentadaref=np.copy(imageref[0])
        imagensegmentadaref[~segmentacionesrefbool[i]]=np.nan
        intensidadref=np.nanmean(imagensegmentadaref)
        intensidadesref.append(intensidadref)
        
print(intensidadesref)

#Realizamos todas las segmentaciones en las imágenes prospectivas para 1 movimiento. Calculamos RC
dic={}
dic['Names']=direct
for j in range(0,len(images)):
    #intensidades=[]
    RCtotal=[]
    for i in range(0,len(seg)):
        imagensegmentada=np.copy(images[j])
        imagensegmentada[~segmentacionesbool[i]]=np.nan
        intensidad=np.nanmean(imagensegmentada)
        RC=intensidad/intensidadesref[i]
        RCtotal.append(RC)
        #intensidades.append(intensidad)
    dic[pets[j]]=RCtotal


#Guardamos valores de RC en un .csv
keylist=dic.keys()
valuelist=dic.values()
with open('M02_prosp.csv', 'w') as f:
    for key in dic.keys():
        #key.replace("[","")
        f.write("%s,%s\n"%(key,dic[key]))
quit()
#fig=plt.figure()
#plt.imshow(imagensegmentada[:,:,60])
#plt.show()




