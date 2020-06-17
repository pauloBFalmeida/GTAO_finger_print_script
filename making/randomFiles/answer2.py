from PIL import ImageGrab
from PIL import Image # test
from time import sleep	# test
import numpy as np
import cv2

sleep(2)

def get_imgs_parts(img):
	_, threshold = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
	contours,_ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	# add perimeter to contours
	per_contours = []
	for cnt in contours:
		perimeter = cv2.arcLength(cnt,True)
		per_contours.append( (perimeter, cnt) )
	# sort by perimeter
	per_contours.sort(key=(lambda x: x[0]))
	# find the 8 contours with the min difference between
	seq_i = 0
	seq_difference = 9999
	for i in range(len(per_contours)-8):
		difference = per_contours[i+8][0] - per_contours[i][0]
		# divide by the high value, so difference is related to the number
		# otherwise the first values would be the smallest
		difference /= per_contours[i+8][0]
		if difference < seq_difference:
			seq_i = i
			seq_difference = difference
	# select just the digital rects
	rect_contours = per_contours[seq_i:seq_i+8]
	# remove the perimeter
	for i in range(len(rect_contours)): rect_contours[i] = rect_contours[i][1]
	# draw the contours in the original image # test
	for cnt in rect_contours:
		cv2.drawContours(img, cnt, -1, (200, 200, 0), 2)
	# # show the image
	# cv2.imshow('Contours', img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# crop without the margin
	imgs_parts = []
	for i in range(len(rect_contours)):
		c = rect_contours[i]
		x,y,w,h = cv2.boundingRect(c)
		# remove the margin
		margin = 6
		x += margin
		y += margin
		w -= margin*2
		h -= margin*2
		# crop
		img_part = img[y:y+h, x:x+w]
		# add (x, y, img)
		imgs_parts.append( (x, y, img_part) )
	# sort by y then by x (y*10 + x)
	imgs_parts.sort(key=(lambda i: i[1]*10 + i[0]))
	# remove the x y
	for i in range(len(imgs_parts)): imgs_parts[i] = imgs_parts[i][2]
	# # saves	test
	# for i in range(len(imgs_parts)):
	# 	im = imgs_parts[i]
	# 	cv2.imwrite('part_{}.png'.format(i), im)
	# return
	return imgs_parts

def save_seq_file(belongs):
	with open('answers.txt', 'w') as file:
		# start up left
		last_i = 0	# line
		last_j = 0	# column
		for curr_i in range(4):		# each line
			for curr_j in range(2):	# each column
				if belongs[curr_i*2 + curr_j]:
					# see how much it move since last
					move_lines = curr_i - last_i
					move_columns = curr_j - last_j
					# write in file
					for _ in range(move_lines):
						file.write('down\n')
					if move_columns > 0:
						file.write('right\n')
					elif move_columns < 0:
						file.write('left\n')
					# hit enter
					file.write('enter\n')
					# updates last i and j
					last_i = curr_i
					last_j = curr_j

def main():
	img = ImageGrab.grab()	# screenshot
	# img = Image.open('teste.jpg', 'r')	# test

	img = img.resize((1200,700))
	# img = img.resize((1000,700))
	img_np = np.array(img) # array obtained from conversion
	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

	belongs = [False for _ in range(8)]
	for i in range(1,4+1):
		# Load an color image in grayscale
		img = cv2.imread('pictures/fingers/'+str(i)+'.png',0)

		for s in range(2, 20, 1):
			s = s/10
			width = int(img.shape[1] * s)
			height = int(img.shape[0] * s)
			im = cv2.resize(img, (width, height))

			result = cv2.matchTemplate(im, frame, cv2.TM_SQDIFF_NORMED)
			# We want the minimum squared difference
			mn,_,mnLoc,_ = cv2.minMaxLoc(result)

			# Draw the rectangle:
			# Extract the coordinates of our best match
			MPx,MPy = mnLoc
			# Step 2: Get the size of the template. This is the same size as the match.
			trows,tcols = im.shape[:2]
			# Step 3: Draw the rectangle on large_image
			cv2.rectangle(frame, (MPx,MPy),(MPx+tcols,MPy+trows),(200,250,255),2)
			# print(mnLoc)

			# cv2.imshow('try'+str(i),im)
			# # Display the original image with the rectangle around the match.
			# cv2.imshow('output'+str(i),frame)
			# # The image is only displayed if we call this
			# cv2.waitKey(0)

			# find
			if mnLoc != (0,0):
				print('finger')
				for j in range(1,4+1):
					im = cv2.imread('pictures/answers/'+str(i)+"/"+str(j)+'.png',0)
					result = cv2.matchTemplate(im, frame, cv2.TM_SQDIFF_NORMED)
					# We want the minimum squared difference
					mn,_,mnLoc,_ = cv2.minMaxLoc(result)
					# find
					if mnLoc != (0,0):
						print(mnLoc)
						belongs[j] = True

	# finish finding images
	save_seq_file(belongs)




# sleep(2)	# test
main()
