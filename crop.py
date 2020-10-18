import cv2
import numpy as np

def pad(img, longside, shortside, portrait):

    diff = longside - shortside
    bef = diff // 2
    if bef == 0: return img
    
    new_img = np.zeros((longside, longside, 3), np.uint8)

    if portrait == 1:
        for i in range(longside):
            for j in range(bef, bef + shortside):
                new_img[i, j] = img[i, j - bef]
    else:
        for i in range(bef, bef + shortside):
            for j in range(longside):
                new_img[i, j] = img[i - bef, j]

    return new_img

def extract(img):
    rows, cols, _ = img.shape

    miny, maxy, minx, maxx = 240, 0, 320, 0

    for i in range(rows):
        for j in range(cols):
            if img[i, j][0] != 0:
                if i < miny: miny = i
                if i > maxy: maxy = i
                if j < minx: minx = j
                if j > maxx: maxx = j
    
    xl = max(maxx - minx, 0)
    yl = max(maxy - miny, 0)

    crop = img[miny:maxy, minx:maxx]
    if xl > yl: longside, shortside, portrait = xl, yl, 0
    else: longside, shortside, portrait = yl, xl, 1
    img = pad(crop, longside, shortside, portrait)
        
    return img

if __name__ == '__main__':
    img = cv2.imread('test.png')
    extract(img)
