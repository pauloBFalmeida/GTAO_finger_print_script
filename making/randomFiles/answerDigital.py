from PIL import ImageGrab
from PIL import Image # test
from time import sleep	# test
import numpy as np
import cv2
import itertools

# sleep(2)

def get_imgs_parts(img):
	# threshold = img
	width, height = img.shape
	print(width)
	print(height)
	print()
	_, threshold = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
	contours,hier = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	# add perimeter to contours
	per_contours = []
	for i in range(len(contours)):
		cnt = contours[i]
		perimeter = cv2.arcLength(cnt,True)
		if hier[0,i,3] == -1 and perimeter > width//2 and perimeter < width*11//12:
			print(perimeter)
			per_contours.append( (perimeter, cnt) )

	# # show the image
	# cv2.drawContours(img, nada, -1, (255,255,255))
	# cv2.imshow('conts', img)
	# cv2.waitKey(0)

	# sort by perimeter
	per_contours.sort(key=(lambda x: x[0]))
	# find the 8 contours with the min difference between
	seq_i = 0
	seq_difference = 9999
	for i in range(len(per_contours)-8):
		difference = per_contours[i+8][0] - per_contours[i][0]
		# divide by the high value, so difference is related to the number
		# otherwise the first values would be the smallest
		difference /= per_contours[i][0]
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

	# show the image
	cv2.imshow('Contours', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

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

def img_to_list(img):
	output = []
	width, height = img.shape
	for y in range(height):
		for x in range(width):
			output.append(img[x,y])
	return output

def compressor(img, block_size):
	width, height = img.shape
	# calculate new width and height for the block
	width_block = (width//block_size)
	height_block = (height//block_size)

	# compress each line
	comp = []
	for y in range(height_block*block_size):
		line_comp = [0 for _ in range(width_block)]
		for x in range(width_block*block_size):
			line_comp[x//block_size] += img[x,y]
		comp.append(line_comp)

	# compress columns by sum block_size lines at a time
	compressed = []
	for y_b in range(height_block):	# each line of block
		column_comp = [0 for _ in range(width_block)]
		for k_b in range(block_size):	# each line inside the block
			for x in range(width_block):	# each column (block)
				y = y_b*block_size + k_b
				column_comp[x] += comp[y][x]
		compressed.append(column_comp)

	#
	data = []
	for line_comp in compressed:
		for x in line_comp:
			data.append(x//block_size)

	# show
	new_im = Image.new('L', (width_block, height_block))
	new_im.putdata(data)
	new_im.show()

	# end
	return (width_block, height_block, data)




# return if l1 contains l2 with some threshold
def list_contains(l1, l2, threshold):
	for i in range(len(l1)):
		j = 0
		while(abs(l1[i+j] - l2[j]) <= threshold):
			j += 1
			if j == len(l2): return True		# end of sublist
			if i+j == len(l1): return False		# end of list1
			# print(i)
			# print(j)
			# print()
	return False

def image_inside(img, template, threshold):
	# pass by each element of template
	w_img, h_img, comp_img = img
	w_tem, h_tem, comp_tem = template

	# # show
	# new_im = Image.new('L', (w_img, h_img))
	# im_data = [x//block_size for x in comp_img]
	# new_im.putdata(im_data)
	# new_im.show()


	img_i = 0
	for tem_i in range(h_tem):
		line_tem = comp_tem[tem_i*w_tem:(tem_i+1)*w_tem]
		line_img = comp_img[img_i*w_img:(img_i+1)*w_img]
		if list_contains(line_tem, line_img, threshold):
			img_i += 1
			if img_i == h_img: return True
			if tem_i == h_tem: return False
		else:
			tem_i -= img_i -1
			img_i = 0
	return False

# def image_inside(img, tem):
# 	threshold = int( 255* 1/5 )
#
# 	w_img, h_img = img.shape
# 	w_tem, h_tem = tem.shape
#
# 	img_im = img_to_list(img)
# 	tem_im = img_to_list(tem)
#
# 	img_i = 0
# 	for tem_i in range(h_tem):
# 		line_tem = tem_im[tem_i*w_tem:(tem_i+1)*w_tem]
# 		line_img = img_im[img_i*w_img:(img_i+1)*w_img]
# 		if list_contains(line_tem, line_img, threshold):
# 			img_i += 1
# 			if img_i == h_img: return True
# 			if tem_i == h_tem: return False
# 		else:
# 			tem_i -= img_i -1
# 			img_i = 0
# 	return False


def main():
	# img = ImageGrab.grab()	# screenshot
	img = Image.open('1.png', 'r')	# test
	img = img.resize((1000,600))	# last 3

	# img = img.resize((1400,600))
	# img = img.resize((1400,700))	# finds top
	# img = img.resize((1200,600))	# bottom 2
	# img = img.resize((1200,550))	# last 3
	# frame =  cv2.resize(frame, (1800, 900))


	img_np = np.array(img) # array obtained from conversion
	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
	# _, frame = cv2.threshold(frame, 33, 255, cv2.THRESH_BINARY) # test
	#
	# frame = cv2.resize(frame, (900, 700))

	# crops image in parts and finger
	height, width = frame.shape
	parts_image = frame[int(height*0.2):int(height*0.8), int(width*0.2):int(width*0.45)]
	finger_image = frame[int(height*0.1):int(height*0.7), int(width*0.45):int(width*0.75)]
	# cv2.imwrite('finger_image.png', finger_image)	# test

	# cv2.imshow('finger_image', finger_image)
	# cv2.imshow('parts_image', parts_image)
	# cv2.waitKey(0)


	imgs_parts = get_imgs_parts(parts_image)


	block_size = 3
	# threshold = int( block_size*255* 1/5 )
	threshold = 120
	# compress template
	comp_temp = compressor(finger_image, block_size)

	belongs = [False for _ in range(len(imgs_parts))]
	# for i in range(len(imgs_parts)):
	for i in range(8):
	# for i in range(1):
		im_part = imgs_parts[i]
		comp_part = compressor(im_part, block_size)

		belongs[i] = image_inside(comp_part, comp_temp, threshold)

	print(belongs)
	print([False, True, False, True, True, True, False, False])
	# save_seq_file(belongs)



main()
