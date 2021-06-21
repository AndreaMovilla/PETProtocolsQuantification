import numpy as np
import nrrd
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

	imagenes_nrrd = []
	for i in range(0, len(barlist)):
		imagenes_nrrd.append(nrrd.read(barlist[i])[0])

	return imagenes_nrrd


def directories(path):
	foodir = path
	barlist = list()

	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				barlist.append(join(root, f))
	nombres = []

	for i in range(0, len(barlist)):
		nombres.append(barlist[i][-7:-5])
	return nombres


def names(path):
	foodir = path
	names = list()
	for root, dirs, files in walk(foodir):
		for f in files:
			if splitext(f)[1].lower() == ".nrrd":
				f.replace(".nrrd","")
				names.append(f)
	return names



def thresholdseg(seg, image, voxeldim):
	segmentbool = seg.astype('bool')
	imageseg = np.copy(image)
	imageseg[~segmentbool] = np.nan
	vmax = np.nanmax(imageseg)
	coord = np.where(imageseg == vmax)
	#print('coord_first',coord)
	# Calculamos hasta que punto en el eje z tenemos valores superiores al 70%
	testz_down = 0
	while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0]][coord[1][0]][coord[2][0] + testz_down]:
		testz_down = testz_down - 1
	testz_down = testz_down + 1

	testz_up = 0
	while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0]][coord[1][0]][coord[2][0] + testz_up]:
		testz_up = testz_up + 1
	testz_up = testz_up - 1

	testy_down = 0
	testy_up = 0
	# Calculamos hasta que punto en el eje y tenemos valores superiores al 70%
	while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0]][coord[1][0] + testy_up][coord[2][0]]:
		testy_up = testy_up + 1
	testy_up = testy_up - 1

	while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0]][coord[1][0] + testy_down][
		coord[2][0]]:
		testy_down = testy_down - 1
	testy_down = testy_down + 1

	# Calculamos hasta que punto en el eje x tenemos valores superiores al 70% ligado a los ejes z e y. Obtenemos las coordenadas de todos los puntos
	coord1 = []
	for j in range(testz_down, testz_up):
		for i in range(testy_down, testy_up):
			testx_up = 0
			testx_down = -1
			while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0] + testx_up][coord[1][0] + i][
				coord[2][0] + j]:
				coord1.append((coord[0][0] + testx_up, coord[1][0] + i, coord[2][0] + j))
				testx_up = testx_up + 1
			while image[coord[0][0]][coord[1][0]][coord[2][0]] * 0.7 < image[coord[0][0] + testx_down][coord[1][0] + i][
				coord[2][0] + j]:
				coord1.append((coord[0][0] + testx_down, coord[1][0] + i, coord[2][0] + j))
				testx_down = testx_down + 1

	# Calculamos la intensidad media de todos los puntos obtenidos
	intensidades70 = []
	#print('coord',coord1)
	for i in range(0, len(coord1)):
		intensidad70 = image[coord1[i][0]][coord1[i][1]][coord1[i][2]]
		intensidades70.append(intensidad70)
	#print('is:',intensidades70)
	media70 = np.mean(intensidades70)
	valor40 = 0.4 * media70

	# Calculamos hasta que punto en el eje z tenemos valores superiores al 40% de la media del 70%
	testz_down = 0
	testz_up = 0
	while valor40 < image[coord[0][0]][coord[1][0]][coord[2][0] + testz_down]:
		testz_down = testz_down - 1
	testz_down = testz_down + 1

	while valor40 < image[coord[0][0]][coord[1][0]][coord[2][0] + testz_up]:
		testz_up = testz_up + 1
	testz_up = testz_up - 1

	# Calculamos hasta que punto en el eje y tenemos valores superiores al 40% de la media del 70%
	testy_down = 0
	testy_up = 0
	while valor40 < image[coord[0][0]][coord[1][0] + testy_up][coord[2][0]]:
		testy_up = testy_up + 1
	testy_up = testy_up - 1

	while valor40 < image[coord[0][0]][coord[1][0] + testy_down][coord[2][0]]:
		testy_down = testy_down - 1
	testy_down = testy_down + 1

	# Calculamos hasta que punto en el eje x tenemos valores superiores al 40% de la media del 70% ligado a los ejes z e y. Obtenemos las coordenadas de todos los puntos
	coord2 = []
	for j in range(testz_down, testz_up):
		for i in range(testy_down, testy_up):
			testx_up = 0
			testx_down = -1
			while valor40 < image[coord[0][0] + testx_up][coord[1][0] + i][coord[2][0] + j]:
				coord2.append((coord[0][0] + testx_up, coord[1][0] + i, coord[2][0] + j))
				testx_up = testx_up + 1
			while valor40 < image[coord[0][0] + testx_down][coord[1][0] + i][coord[2][0] + j]:
				coord2.append((coord[0][0] + testx_down, coord[1][0] + i, coord[2][0] + j))
				testx_down = testx_down - 1

	#Con las coordenadas obtenemos la segmentación
	imageseg2=np.copy(image)*0
	for i in range(0,len(coord2)-1):
		imageseg2[coord2[i][0]][coord2[i][1]][coord2[i][2]]=1
	#Obtenemos el volumen de la segmentación
	numerovoxels = len(coord2)
	volumen = numerovoxels * (voxeldim**3) / 1000
	return volumen, imageseg2
