#

import math
import numpy as np
import sys

######################################
# Pixel Resolution in deg.
######################################
def ResoInDeg_250m():
#    return 0.0020833334
    return 0.0020833333333333333
def ResoInDeg_1km():
#    return 0.008333334
    return 0.0083333333333333333

######################################
# Lat, Lng <-> sgli tile image (x, y)
#   conversion
######################################
#Lat,Lon -> image x ,y
def sgli_ll2tile_B1(NumPix, lng, lat):
	d = 180.0 / NumPix /18.0
	
	NPO = 180.0 / d * 2.0
	
	NPi = NPO * math.cos(lat * math.pi / 180.0)
	
	Global_lin = (90.0 - lat) / d + 0.5
	
	Global_col = lng * NPi / 360.0 + NPO / 2.0 + 0.5
	
#	dlin = fmod(Global_lin - 0.5, NumPix)
#	dcol = fmod(Global_col - 0.5, NumPix)
	dlin = (Global_lin - 0.5) % NumPix
	dcol = (Global_col - 0.5) % NumPix
	
	V = (int)((Global_lin - dlin) / NumPix)
	H = (int)((Global_col - dcol) / NumPix)
	
#	imgY = fmod(Global_lin - 0.5, NumPix) + 0.5
#	imgX = fmod(Global_col - 0.5, NumPix) + 0.5
	imgY = (Global_lin - 0.5) % NumPix + 0.5
	imgX = (Global_col - 0.5) % NumPix + 0.5
	
	return V, H, imgX, imgY

def sgli_ll2tile_B0(NumPix, lng, lat):
    V, H, imgX, imgY = sgli_ll2tile_B1(NumPix, lng, lat)
    return V, H, imgX-0.5, imgY-0.5
#    return V, H, imgX-1.0, imgY-1.0


# tile image x ,y -> Lat,Lon
def sgli_tile2ll_B1(NumPix, V, H, imgX, imgY):
	d = 180.0 / NumPix / 18.0
	
	NL = 180.0 / d
	
	NPO = 180.0 / d * 2.0
	
	LineTotal = imgY + V * NumPix
	ColTotal  = imgX + H * NumPix
	
	lat = 90.0 - (LineTotal - 0.5) * d
	
	NPi = NPO * math.cos( lat * math.pi / 180.0 )
	
	lng = 360.0 / NPi * (ColTotal - NPO/2.0 - 0.5)
	
	return lng, lat

def sgli_tile2ll_B0(NumPix, V, H, imgX, imgY):
    lng, lat = sgli_tile2ll_B1(NumPix, V, H, imgX+0.5, imgY+0.5)
#    lng, lat = sgli_tile2ll_B1(NumPix, V, H, imgX+1.0, imgY+1.0)
    return lng, lat

######################################
# Area specification
######################################

#*************************************
# Adjusted UL pos lng, lat 
#
#    UL(lng,lat)
#         |--------------|
#         |              |
#         |              |
#         |              |
#         |         x    |
#         |              |
#         |--------------|
#
#   if given lng, lat fall on 'x' pos of the pixel, 
#      this function return UL(lng, lat)
#
def sgli_GetPixULllFromGivenll(Numpix, lng, lat):
    V, H, imgX, imgY = sgli_ll2tile_B1(Numpix, lng, lat)
    lng, lat = sgli_tile2ll_B1(Numpix, V, H, imgX-0.5, imgY-0.5)
    return lng, lat



# test main
'''
V, H, imgX, imgY = sgli_ll2tile_B1(4800, 140.346080, 41.262984)
print('sgli_ll2tile_B1(4800, 140.346080, 41.262984)')
print('T{0:02d}{1:02d}'.format(V, H))
print('imgX = {}, imgY = {}'.format(imgX, imgY))

lng, lat = sgli_tile2ll_B1(4800, V, H, imgX, imgY)
print('sgli_tile2ll_B1(4800, V, H, imgX, imgY)')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

V, H, imgX, imgY = sgli_ll2tile_B0(4800, 140.346080, 41.262984)
print('sgli_ll2tile_B0(4800, 140.346080, 41.262984)')
print('T{0:02d}{1:02d}'.format(V, H))
print('imgX = {}, imgY = {}'.format(imgX, imgY))

lng, lat = sgli_tile2ll_B0(4800, V, H, imgX, imgY)
print('sgli_tile2ll_B0(4800, V, H, imgX, imgY)')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

print('--------------------------------------')

lng, lat = sgli_tile2ll_B1(4800, 4, 28, 1, 1)
print('sgli_tile2ll_B1(4800, 04, 28, 1, 1)')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

lat, lng = sgli_GetPixULllFromGivenll(4800, lng, lat)
print('sgli_GetPixULllFromGivenll(4800, lng, lat)')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

print('--------------------------------------')

lng, lat = sgli_tile2ll_B0(4800, 4, 28, 0.5, 0.5)
print('sgli_tile2ll_B1(4800, 4, 28, 0.5, 0.5')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

lat, lng = sgli_GetPixULllFromGivenll(4800, lng, lat)
print('sgli_GetPixULllFromGivenll(4800, lng, lat)')
print('lng = {}, lat = {}\n\n'.format(lng, lat))

'''
