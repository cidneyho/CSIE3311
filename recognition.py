import cv2
import numpy as np

def recognize(img, knn):
    if img.shape == (0, 0, 3): return -1
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (28, 28), cv2.INTER_LINEAR)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = img.flatten()
    img = img.astype(np.float32)
	
    data = np.array([img])
    ret, output, neighbours, distance = knn.findNearest(data, k = 5)
    return int(output[0][0])

if __name__ == '__main__':
    knn = cv2.ml.KNearest_load('knn')
    img = cv2.imread('test.png')
    print(recognize(img, knn))