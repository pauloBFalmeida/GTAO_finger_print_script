from PIL import Image, ImageGrab, ImageDraw
from time import time_ns

def test():
	# im = ImageGrab.grab()
	im = Image.open('exemple.jpg', 'r')	# test

	im = im.convert('L')
	im = im.resize((600,400))
	im = Image.eval(im, (lambda x: 0 if x<20 else x))
	width,height = im.size
	parts = im.crop((width*0.2, height*0.2,  width*0.45, height*0.8))
	finger = im.crop((width*0.45, height*0.1,  width*0.75, height*0.7))
	# parts.show()
	# finger.show()
	boxes = extract_from_box(parts)
	parts_inside = []
	for box in boxes:
		part = parts.crop(box)
		parts_inside.append(is_inside(part, finger, 10))


# def inside_list(sublist, biglist, variation):
# 	if len(sublist) == 0: return True
# 	if len(sublist) > len(biglist): return False
# 	s = sublist[0]
# 	for i in range(len(biglist)):
# 		b = biglist[i]
# 		if abs(b - s) <= variation:
# 			return inside_list(sublist[1:], biglist[i+1:], variation)


# def inside_list(sublist, biglist, variation):
# 	if len(sublist) == 0: return True
# 	if len(sublist) > len(biglist): return False
# 	s = sublist[0]
# 	for i in range(len(biglist)):
# 		b = biglist[i]
# 		if abs(b - s) <= variation:
# 			return inside_list(sublist[1:], biglist[i+1:], variation)

def is_inside(part, finger, variation):
	# finger
	f_data = finger.getdata()
	f_width, f_height = finger.size
	# part
	p_data = part.getdata()
	p_width, p_height = part.size
	p_line_i = 0

	# # line index of each line of pixels in the finger
	# for f_line_i in range(f_height):
	# 	# list[first : last], last is not included
	# 	f_line = f_data[f_line_i*f_width : (f_line_i+1)*f_width]
	#
	# 	p_line = p_data[p_line_i*p_width : (p_line_i+1)*p_width]
	# 	if inside_list(p_line, f_line, variation):
	# 		return True
	inside = False

	is_inside = False
	for f_line_i in range(width):
		f_pixel = f_data[f_line_i]	# get pixel from finger line
		if abs(f_pixel - p_data[0]) <= variation:
			for j in range(len(p_data)-1):
				is_inside = abs(f_data[f_line_i + j] - p_data[j]) <= variation
			if not is_inside:
				break
		if is_inside:
			print('inside')
			continue

def extract_from_box(im):
	width,height = im.size
	data = im.getdata()
	start = -1	# start of the line
	in_line = 0	# size of pixels in the line
	lines = []	# (start, end) of each line
	for i in range(len(data)):
		if data[i] != 0:		# not black pixel
			if start == -1:
				start = i
			in_line += 1		# add 1 to pixels in line
		else:					# black pixel
			if in_line > width//5 and in_line < width//2:	# size of the line
				lines.append( (start, start+in_line) )
			in_line = 0	# reset line
			start = -1

	# lets every line 1 pixel thick
	prev_lines = [(-99, -99), (-99, -99)]
	odd = True
	for line in lines.copy():
		# index of (line, column)
		curr_line = (line[0] // width, line[0] % width)
		prev_line = prev_lines[0 if odd else 1] # jumps one line (lines in same matrix line)
		if abs(curr_line[0] - prev_line[0]) < 3 and abs(curr_line[1] - prev_line[1]) < 3:
			lines.remove(line)
		prev_lines[0 if odd else 1] = curr_line
		odd = not odd

	# lines but in x,y vertices  (line = height, column = width)
	linesxy = []
	for line in lines:
		start = (line[0] % width, line[0] // width)
		end   = (line[1] % width, line[1] // width)
		linesxy.append( (start, end) )

	# get boxes (left, upper, right, and lower) from lines
	boxes = []
	for i in range(0,len(linesxy)-1,4):	# jumps 4
		for j in range(2):	# do for the 2 lines in the same matrix line
			i += j
			left, upper = linesxy[i][0]
			right, lower = linesxy[i+2][1]
			# remove the margin
			margin = 3
			left += margin
			upper -= margin
			right -= margin
			lower += margin
			boxes.append( (left, upper, right, lower) )

	# # show white rects for the parts
	# ima = Image.new('L', im.size, color=0)
	# draw = ImageDraw.Draw(ima)
	# for xy in boxes:
	# 	draw.rectangle(xy, fill=(255), width=0)
	# ima.show()
	return boxes

def main():

	file_name = 'answers.txt'
	with open(file_name, 'w') as file:
		file.write('right')


# ############
t1 = time_ns()

# main()
# test()
# print (is_inside([1,2,3], [3,1,2,4,5,3], 0))


t2 = time_ns()
td = (t2 - t1) / 10**9
print(td)
