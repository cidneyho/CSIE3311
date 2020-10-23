import cv2
import numpy as np
from recognition import recognize
from crop import extract

threshold = 12		# threshold for illuminance
waittime = 1200		# waiting time before next detection

knn = cv2.ml.KNearest_load('knn')

gapcount = 0		# count to ensure input is done
gapcutoff = 64

# 選擇攝影機
cap = cv2.VideoCapture(0)
trackpad = np.zeros((240, 320, 3), np.uint8)
trackpad_flip = trackpad

while(True):
	# 從攝影機擷取一張影像
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	
	sizes = [(cv2.contourArea(cnt), cnt) for cnt in contours]
	if sizes == []: 
		gapcount = gapcount + 1
		if gapcount > gapcutoff: 
			gapcount = 0
			# start digit recognition
			toRec = extract(trackpad)
			result = recognize(toRec, knn)
			if result == -1: continue
			text = str(result)
			cv2.putText(trackpad_flip, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
			cv2.imshow('trackpad', trackpad_flip)
			cv2.waitKey(waittime)

			trackpad = np.zeros((240, 320, 3), np.uint8)
			trackpad_flip = trackpad
		
		frame_flip = cv2.flip(frame, 1)
		cv2.imshow('frame', frame_flip)
		cv2.imshow('trackpad', trackpad_flip)
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
			cv2.circle(trackpad, (cx, cy), 10, (255, 255, 255), -1)
			trackpad_flip = cv2.flip(trackpad, 1)

	# 顯示圖片
	frame_flip = cv2.flip(frame, 1)
	cv2.imshow('frame', frame_flip)
	cv2.imshow('trackpad', trackpad_flip)

	# 若按下 q 鍵則離開迴圈
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()