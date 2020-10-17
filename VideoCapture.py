import cv2
import numpy as np

gapcount = 0
gapcutoff = 32

# 選擇攝影機
cap = cv2.VideoCapture(0)
trackpad = np.zeros((240, 320, 3), np.uint8)

while(True):
	# 從攝影機擷取一張影像
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	
	sizes = [(cv2.contourArea(cnt), cnt) for cnt in contours]
	if sizes == []: 
		gapcount = gapcount + 1
		if gapcount > gapcutoff: 
			gapcount = 0
			trackpad = np.zeros((240, 320, 3), np.uint8)
		
		cv2.imshow('frame', frame)
		cv2.imshow('trackpad', trackpad)
		cv2.waitKey(1)
		continue

	biggestCnt = max(sizes, key=lambda x: x[0])[1]

	cnt = biggestCnt
	cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)

	M = cv2.moments(cnt)
	if M['m00'] != 0: 
		cx = int(M['m10'] / M['m00'])
		cy = int(M['m01'] / M['m00'])
		cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

		if 0 < cx < 240 and 0 < cy < 320: 
			cv2.circle(trackpad, (cx, cy), 6, (255, 255, 255), -1)

	# 顯示圖片
	cv2.imshow('frame', frame)
	cv2.imshow('trackpad', trackpad)

	# 若按下 q 鍵則離開迴圈
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()