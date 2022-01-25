import numpy as np
import cv2

'''
draw obj on src canvas
obj should be of size (2n-1) and the pivot is in the center
and of shape (H,W)
x, y as pixel(screen) coordinate
'''
def draw(src, obj, x, y, strategy = 'overlap'):
    if isinstance(src,np.ndarray) and isinstance(obj,np.ndarray):
        pvx = obj.shape[-1]//2
        pvy = obj.shape[-2]//2

        t_offset = min(pvy, y)
        l_offset = min(pvx, x)
        r_offset = min(pvx+1, src.shape[-1]-x)
        b_offset = min(pvy+1, src.shape[-2]-y)

        if strategy == 'add':
            src[y-t_offset:y+b_offset,x-l_offset:x+r_offset] += \
                obj[pvy-t_offset:pvy+b_offset,pvx-l_offset:pvx+r_offset]
        else:
            src[y-t_offset:y+b_offset,x-l_offset:x+r_offset] = \
                obj[pvy-t_offset:pvy+b_offset,pvx-l_offset:pvx+r_offset]


'''
returns z value of inverse square graph as 2d array
the distance is taxi distance, since fish cannot move diagonally
eq : z = a/(b+(|x|+|y|)^2), a/b at x=0,y=0
    and clip z > c 
size should be an odd value
'''
def getInverseSquareMat(size,a,b,c):
    hsize = size//2
    x = np.abs(np.arange(-hsize,hsize+1,1))
    y = np.abs(np.arange(-hsize,hsize+1,1))
    xv,yv = np.meshgrid(x,y)

    ret = a/((xv+yv)**2+b)
    ret[ret>c] = c
    return ret
    

