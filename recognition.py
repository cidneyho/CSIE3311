import cv2
import numpy as np

def knn_training(img):
	img = cv2.imread(img)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	divide = list(np.hsplit(i,100) for i in np.vsplit(gray, 50))
	array = np.array(divide)
	
	train_data = array[:, :50].reshape(-1,400).astype(np.float32)
	
	k = np.arange(10)
	
	train_labels = np.repeat(k, 250)[:, np.newaxis]
	
	knn = cv2.ml.KNearest_create()
	knn.train(train_data, cv2.ml.ROW_SAMPLE, train_labels)
	
	return knn

def recognize(img, knn):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (20, 20), cv2.INTER_LINEAR)
	img = img.flatten()
	img = img.astype(np.float32)
	
	L = [img]
	data = np.array(L)
	ret, output, neighbours, distance = knn.findNearest(data, k = 3)
	return int(output[0][0])
	
if __name__ == '__main__':
	knn = knn_training('training.png')
	img = cv2.imread('test.png')
	print(recognize(img, knn))