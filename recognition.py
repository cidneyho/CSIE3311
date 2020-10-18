import cv2
import numpy as np

def recognize(img, knn):
    if img is None: return '?'
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (28, 28), cv2.INTER_LINEAR)
    img = img.flatten()
    img = img.astype(np.float32)
	
    data = np.array([img])
    ret, output, neighbours, distance = knn.findNearest(data,k = 3)
    return int(output[0][0])

if __name__ == '__main__':
    knn = cv2.ml.KNearest_load('knn')
    img = cv2.imread('test.png')
    print(recognize(img, knn))