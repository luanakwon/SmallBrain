import numpy as np
import cv2

def getInverseSquareMat(size,a,b):
    hsize = size//2
    x = np.abs(np.arange(-hsize,hsize+1,1))
    y = np.abs(np.arange(-hsize,hsize+1,1))
    xv,yv = np.meshgrid(x,y)
    xv[hsize,hsize] = 1

    ret = a/((xv+yv)**2)
    ret[ret>b] = b
    return ret

print(getInverseSquareMat(5,10,2))