from sys import argv
from numpy import array
from pyautogui import screenshot
from time import sleep
import configparser
import cv2

# # # # # # # # # # # # # # # finger print Solution # # # # # # # # # # # # # #

class Solution_fingerprint():
	def __init__(self):
		# start configparser
		Config = configparser.ConfigParser()
		Config.read("settings.ini")
		# get configs
		self.showContours = Config.getboolean("Fingerprint", "showContours")
		self.threshold = Config.getint("Fingerprint", "threshold")
		self.margin = Config.getint("Fingerprint", "margin")
		resize_size = Config.get("Fingerprint", "resize_size").split(',')
		self.resize_size = tuple(map(int, resize_size))
		# crop parts
		self.parts_str_h = Config.getfloat("Fingerprint", "parts_str_h")
		self.parts_end_h = Config.getfloat("Fingerprint", "parts_end_h")
		self.parts_str_w = Config.getfloat("Fingerprint", "parts_str_w")
		self.parts_end_w = Config.getfloat("Fingerprint", "parts_end_w")

	def get_imgs_parts(self, img):
		_, threshold = cv2.threshold(img, self.threshold, 255, cv2.THRESH_BINARY)
		contours,hier = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		width, height = img.shape
		area_contours = []
		for i in range(len(contours)):
			cnt = contours[i]
			area = cv2.contourArea(cnt)
			perimeter = cv2.arcLength(cnt,True)
			if hier[0,i,3] == -1:
				if area > width*10 and perimeter > width//2 and perimeter < width:
					area_contours.append( (area, cnt) )
		# sort by area
		area_contours.sort(key=(lambda x: x[0]))
		# find the 8 contours with the min difference between area
		seq_i = 0
		seq_difference = 9999
		for i in range(len(area_contours)-8):
			difference = area_contours[i+8][0] - area_contours[i][0]
			# divide by the high value, so difference is related to the number
			# otherwise the first values would be the smallest
			difference /= area_contours[i+8][0]
			if difference < seq_difference:
				seq_i = i
				seq_difference = difference
		# select just the digital rects
		rect_contours = area_contours[seq_i:seq_i+8]
		# remove the area
		for i in range(len(rect_contours)): rect_contours[i] = rect_contours[i][1]

		# # draw the contours in the original image
		if self.showContours:
			for cnt in rect_contours:
				cv2.drawContours(img, cnt, -1, (200, 200, 0), 2)
			cv2.imshow('Contours', img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		# crop without the margin
		imgs_parts = []
		for i in range(len(rect_contours)):
			c = rect_contours[i]
			x,y,w,h = cv2.boundingRect(c)
			# remove the margin
			x += self.margin
			y += self.margin
			w -= self.margin*2
			h -= self.margin*2
			# crop
			img_part = img[y:y+h, x:x+w]
			# add (x, y, img)
			imgs_parts.append( (x, y, img_part) )
		# sort by y then by x (y*10 + x) to get fist the line and then the column
		imgs_parts.sort(key=(lambda i: i[1]*10 + i[0]))
		# remove the x y
		for i in range(len(imgs_parts)): imgs_parts[i] = imgs_parts[i][2]
		# return just images
		return imgs_parts

	def save_seq_file(self,belongs):
		with open('answers_finger.txt', 'w') as file:
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

	def same_img(self, img1, img2):
		height, width = img1.shape
		img2 = cv2.resize(img2, (width, height))
		_, img1 = cv2.threshold(img1, self.threshold, 255, cv2.THRESH_BINARY)
		_, img2 = cv2.threshold(img2, self.threshold, 255, cv2.THRESH_BINARY)
		# difference of each line
		dif = []
		for y in range(height):
			sum_1 = 0
			sum_2 = 0
			for x in range(width):
				sum_1 += img1[y,x]
				sum_2 += img2[y,x]
			dif.append(abs(sum_1 - sum_2))
		# return average difference
		return (sum(dif) // len(dif))

	def main(self):
		img = screenshot()
		img_np = array(img) # array obtained from conversion
		frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
		# resize
		frame = cv2.resize(frame, self.resize_size)

		# crops image in parts and finger
		height, width = frame.shape
		parts_image = frame[int(height*self.parts_str_h):int(height*self.parts_end_h), int(width*self.parts_str_w):int(width*self.parts_end_w)]

		imgs_parts = self.get_imgs_parts(parts_image)

		belongs = [False for _ in range(len(imgs_parts))]
		all_fingers = []
		for i in range(1,4+1):		# dir related to finger prints
			finger_dir = []
			for j in range(1,4+1):	# the parts imgs
				template = cv2.imread('pictures/'+str(i)+'/'+str(j)+'.png', 0)
				dif_part = []
				for k in range(8):	# the parts from screen
					dif = self.same_img(imgs_parts[k],template)
					dif_part.append( (k, dif) )
				dif_part.sort( key=(lambda x: x[1]) )
				finger_dir.append(dif_part[0])
			all_fingers.append(finger_dir)

		best_match = None
		min_average_dif = 0
		# get just the dif values
		for finger_dir in all_fingers:
			dif = sum( [x[1] for x in finger_dir] ) / len(finger_dir)
			if dif < min_average_dif or best_match == None:
				min_average_dif = dif
				best_match = finger_dir
		# print(best_match)

		for i in [x[0] for x in best_match]:
			belongs[i] = True
		# finish finding images
		self.save_seq_file(belongs)

# # # # # # # # # # # # # # # KEYPAD Solution # # # # # # # # # # # # # # # # #
class Solution_keypad():
	def __init__(self, ):
		# start configparser
		Config = configparser.ConfigParser()
		Config.read("settings.ini")
		# get configs
		self.showDots = Config.getboolean("Keypad", "showDots")
		self.threshold = Config.getint("Keypad", "threshold")
		resize_size = Config.get("Keypad", "resize_size").split(',')
		self.resize_size = tuple(map(int, resize_size))
		# time between each screenshot
		self.sleep_time = Config.getfloat("Keypad", "sleep_time")
		# circle
		self.circle_size = Config.getint("Keypad", "circle_size")
		self.str_x = Config.getint("Keypad", "str_x")
		self.str_y = Config.getint("Keypad", "str_y")
		# crop
		self.str_h = Config.getfloat("Keypad", "str_h")
		self.end_h = Config.getfloat("Keypad", "end_h")
		self.str_w = Config.getfloat("Keypad", "str_w")
		self.end_w = Config.getfloat("Keypad", "end_w")


	def find_dots_pos(self, dots_img):
		_, threshold = cv2.threshold(dots_img, self.threshold, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

		width, height = threshold.shape
		area_contours = []
		for i in range(len(contours)):
			cnt = contours[i]
			area = cv2.contourArea(cnt)
			if area > self.circle_size:
				area_contours.append(cnt)

		dots_pos = []
		for cnt in area_contours:
			# get rect of circle
			x,y,w,h = cv2.boundingRect(cnt)
			# find the center
			x += w//2
			y += h//2
			# get the line and column of the circle grid
			column = round( (x - self.str_x) / self.circle_size)
			line   = round( (y - self.str_y) / self.circle_size)
			# save
			dots_pos.append( (column, line) )

		if self.showDots:
			cv2.imshow('dots', dots_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		# sort by column
		dots_pos.sort(key=(lambda x: x[0]))
		return dots_pos

	def screenshot_dots(self):
		img = screenshot()
		img_np = array(img) # array obtained from conversion
		frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

		# resize
		frame = cv2.resize(frame, self.resize_size)
		# crops image in parts and finger
		height, width = frame.shape
		dots_img = frame[int(height*self.str_h):int(height*self.end_h), int(width*self.str_w):int(width*self.end_w)]
		# return (column, line) of each dot that is lit
		return self.find_dots_pos(dots_img)

	def save_dots_pos_file(self, dots_pos):
		# get just the line from dots_pos (column, line)
		dots_line = [pos[1] for pos in dots_pos]
		with open('answers_dots.txt', 'w') as file:
			# start at top left
			last_line = 0
			for column in range(6):
				curr_line = dots_line[column]
				dif = last_line - curr_line
				for _ in range(abs(dif)):
					if dif < 0:
						file.write("Down\n")
					else:
						file.write("Up\n")
				file.write("Enter\n")
				last_line = curr_line

	def main(self):
		last_dots_pos = None
		not_changed = 0
		while not_changed < (2 / self.sleep_time):	# waits 2 secounds
			dots_pos = self.screenshot_dots()
			not_changed += 1
			# have 6 circles
			if len(dots_pos) == 6:
				# update dots pos
				if last_dots_pos != dots_pos:
					last_dots_pos = dots_pos
					not_changed = 0
			# time between each screenshot
			sleep(self.sleep_time)

		if last_dots_pos != None:
			print(last_dots_pos)
			# save to file
			self.save_dots_pos_file(last_dots_pos)

# # # # # # # # # # # # # # # Main # # # # # # # # # # # # # # # # # # # # # # #
def main():
	hack_type = argv[1]
	# finger print
	if hack_type == '1':
		Solution_fingerprint().main()

	# keypad
	if hack_type == '2':
		Solution_keypad().main()

main()
