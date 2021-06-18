import numpy as np
import nrrd
import pydicom as dicom
from os import walk
from os.path import splitext
from os.path import join


def importnrrd(path):
    foodir = path
    barlist = list()

    for root, dirs, files in walk(foodir):
         for f in files:
             if splitext(f)[1].lower() == ".nrrd":
                barlist.append(join(root, f))

    imagenes_nrrd=[]
    for i in range(0,len(barlist)):
        imagenes_nrrd.append(nrrd.read(barlist[i])[0])
        
    return imagenes_nrrd

def directories(path):
    foodir = path
    barlist = list()

    for root, dirs, files in walk(foodir):
         for f in files:
             if splitext(f)[1].lower() == ".nrrd":
                barlist.append(join(root, f))
    nombres=[]

    for i in range(0,len(barlist)):
        nombres.append(barlist[i][-9:-5])
    return nombres


def names(path): 
    foodir = path
    names=list()
    for root, dirs, files in walk(foodir):
         for f in files:
             if splitext(f)[1].lower() == ".nrrd":
                names.append(f)
    return names



def importdicom(path):
    foodir = path
    barlist = list()

    for root, dirs, files in walk(foodir):
         for f in files:
             if splitext(f)[1].lower() == ".dcm":
                barlist.append(join(root, f))

    imagenes_dicom=[]
    for i in range(0,len(barlist)):
        imagenes_dicom.append(dicom.read_file(barlist[i]))
        
     
 
    return imagenes_dicom