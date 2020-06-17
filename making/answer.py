# from PIL import ImageGrab, Image
import numpy as np
# from time import sleep
import pyautogui
import cv2

def get_imgs_parts(img):
	# threshold = img
	_, threshold = cv2.threshold(img, 33, 255, cv2.THRESH_BINARY)
	contours,hier = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	# add perimeter to contours
	width, height = img.shape
	# per_contours = []
	area_contours = []
	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		# perimeter = cv2.arcLength(cnt,True)
		# if hier[0,i,3] == -1 and perimeter > width//2 and perimeter < width*11//12:
		# 	per_contours.append( (perimeter, cnt) )
		if hier[0,i,3] == -1 and area > 4000:
			area_contours.append( (area, cnt) )
	# sort by perimeter
	area_contours.sort(key=(lambda x: x[0]))
	# find the 8 contours with the min difference between
	seq_i = 0
	seq_difference = 9999
	for i in range(len(area_contours)-8):
		difference = area_contours[i+8][0] - area_contours[i][0]
		# divide by the high value, so difference is related to the number
		# otherwise the first values would be the smallest
		difference /= area_contours[i][0]
		if difference < seq_difference:
			seq_i = i
			seq_difference = difference
	# select just the digital rects
	rect_contours = area_contours[seq_i:seq_i+8]
	# remove the perimeter
	for i in range(len(rect_contours)): rect_contours[i] = rect_contours[i][1]

	# # show the image
	# # draw the contours in the original image # test
	# for cnt in rect_contours:
	# 	cv2.drawContours(img, cnt, -1, (200, 200, 0), 2)
	# cv2.imshow('Contours', img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# crop without the margin
	imgs_parts = []
	for i in range(len(rect_contours)):
		c = rect_contours[i]
		x,y,w,h = cv2.boundingRect(c)
		# remove the margin
		margin = 5
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
	# 	cv2.imwrite('out/part_{}.png'.format(i), im)
	#	cv2.imshow('aee', im)
	#	cv2.waitKey(0)

	# return just images
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
						file.write('Down\n')
					if move_columns > 0:
						file.write('Right\n')
					elif move_columns < 0:
						file.write('Left\n')
					# hit enter
					file.write('Enter\n')
					# updates last i and j
					last_i = curr_i
					last_j = curr_j

def same_img(img1, img2):
	height, width = img1.shape
	img2 = cv2.resize(img2, (width, height))
	_, img1 = cv2.threshold(img1, 33, 255, cv2.THRESH_BINARY)
	_, img2 = cv2.threshold(img2, 33, 255, cv2.THRESH_BINARY)
	# difference of each line
	dif = []
	for y in range(height):
		sum_1 = 0
		sum_2 = 0
		for x in range(width):
			sum_1 += img1[y,x]
			sum_2 += img2[y,x]
		dif.append(abs(sum_1 - sum_2))
	# print((sum(dif) // len(dif)))
	# cv2.imshow('img1',img1)
	# cv2.imshow('img2',img2)
	# cv2.waitKey(0)
	return (sum(dif) // len(dif))

def main():
	# sleep(1)
	# img = Image.open('making/1.png')
	# img = Image.open('tes.png')
	# img = ImageGrab.grab()	# screenshot
	img = pyautogui.screenshot()



	img_np = np.array(img) # array obtained from conversion
	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
	frame = cv2.resize(frame, (1000, 600))

	# crops image in parts and finger
	height, width = frame.shape
	parts_image = frame[int(height*0.2):int(height*0.8), int(width*0.2):int(width*0.45)]
	finger_image = frame[int(height*0.1):int(height*0.7), int(width*0.45):int(width*0.75)]

	imgs_parts = get_imgs_parts(parts_image)

	belongs = [False for _ in range(len(imgs_parts))]
	all_fingers = []
	for i in range(1,4+1):		# dir related to finger prints
		finger_dir = []
		for j in range(1,4+1):	# the parts imgs
			template = cv2.imread('pictures/answers/'+str(i)+'/'+str(j)+'.png', 0)
			dif_part = []
			for k in range(8):	# the parts from screen
				dif = same_img(imgs_parts[k],template)
				dif_part.append( (k, dif) )
			dif_part.sort( key=(lambda x: x[1]) )
			finger_dir.append(dif_part[0])
		all_fingers.append(finger_dir)

	best_match = None
	min_media_dif = 0
	# get just the dif values
	for finger_dir in all_fingers:
		dif = sum( [x[1] for x in finger_dir] ) / len(finger_dir)
		if dif < min_media_dif or best_match == None:
			min_media_dif = dif
			best_match = finger_dir
	# print(best_match)

	for i in [x[0] for x in best_match]:
		belongs[i] = True

	# print(belongs)
	# with open('belongs.txt', 'w') as file:
	# 	for b in belongs:
	# 		msg = 'T' if b else 'F'
	# 		file.write(msg)

	# finish finding images
	save_seq_file(belongs)

main()
