
import pygame
from random import shuffle, randint
pygame.init()

class Recreation():
	def __init__(self):
		# self.width = 1000
		# self.height = 600
		# self.width = 900
		# self.height = 500
		self.width = 1360	# my full screen size
		self.height = 730
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('exemple of hacks')

		# BackGround
		self.background = pygame.image.load("pictures/blank.png")
		self.background = pygame.transform.scale(self.background, (self.width, self.height))

		# # red line in the middle
		# wid = width//9 * 4
		# # wid = width * 0.45
		# pygame.draw.line(screen, (255,0,0), (wid, 0), (wid, height), 3)

		# timer
		self.myfont = pygame.font.SysFont('Arial', 30)
		self.timer_pos = ( int(self.width/4), int(self.height/9))

		# selector starts in top left
		self.selector_i = 0
		self.selector_j = 0
		self.selector_img = pygame.image.load("pictures/selector.png")
		selector_size = ( int(self.width/13), int(self.width/13))
		self.selector_img = pygame.transform.scale(self.selector_img, selector_size)
		# start game
		self.start()

	def start(self):
		# timer
		pygame.time.set_timer(pygame.USEREVENT+2, 1000)
		self.timer = 0
		# generate combination of images from finger print
		self.correct_answer = self.gen_combination_img()
		# saved inputs
		self.saved_inputs = []
		self.clear_saved_inputs()
		# testing inputs rect
		self.testing_inputs_rect = None
		# display
		self.display_update()

	def clear_saved_inputs(self):
		self.saved_inputs = [False for _ in range(8)]
		self.selector_i = 0
		self.selector_j = 0

	def move_selector(self, key_name):
		if   key_name == 'right' and self.selector_j == 0: 	self.selector_j += 1
		elif key_name == 'left' and self.selector_j == 1:	self.selector_j -= 1
		elif key_name == 'down' and self.selector_i < 3:  	self.selector_i += 1
		elif key_name == 'up' and self.selector_i > 0:		self.selector_i -= 1
		elif key_name == 'return':	# enter
			index = self.selector_i*2 + self.selector_j
			self.saved_inputs[index] = not self.saved_inputs[index]

	def testing_inputs(self):
		correct = (self.saved_inputs == self.correct_answer)
		# center square
		color = (0,255,0) if correct else (255,0,0)
		x, y = self.width//2, self.height//2
		size = 10
		self.testing_inputs_rect = (color, (x-size, y-size, size*2, size*2), size)
		if correct:
			pygame.time.set_timer(pygame.USEREVENT+1, 1000)

	def gen_combination_img(self):
		self.finger_pos = ( int(self.width/2), int(self.height/6.5) )
		finger_size = ( int(self.width/5.23), int(self.height/2) )
		self.parts_pos = ( int(self.width/4), int(self.height/4) )
		self.parts_size = ( int(self.width/18.13), int(self.height/9.5) )

		# load a random finger print
		finger_n = randint(1,4)
		finger_img = pygame.image.load("pictures/fingers/"+str(finger_n)+".png")
		self.finger_img = pygame.transform.scale(finger_img, finger_size)

		parts_imgs = []
		# get the image of each answer from the select finger
		for i in range(1,4+1):
			im = pygame.image.load("pictures/answers/"+str(finger_n)+"/"+str(i)+".png")
			parts_imgs.append( (True, im) )
		# get more 4 random images parts
		random_indxs = [x for x in range(1,16+1)]
		for _ in range(4):
			j = random_indxs.pop(randint(0,len(random_indxs)-1))
			im = pygame.image.load("pictures/random/"+str(j)+".png")
			parts_imgs.append( (False, im) )
		# shuffle
		shuffle(parts_imgs)
		# get the correct answers
		correct_answer = [x[0] for x in parts_imgs]
		# get only part image and resize
		self.parts_imgs = []
		for part in parts_imgs:
			im = part[1]
			im = pygame.transform.scale(im, self.parts_size)
			self.parts_imgs.append(im)
		# return only the list of bools
		return correct_answer

	def display_update(self):
		# background
		self.screen.blit(self.background, (0, 0))
		# display finger image
		self.screen.blit(self.finger_img, self.finger_pos)
		# display parts
		for i in range(len(self.parts_imgs)):
			color = (255,255,255) if self.saved_inputs[i] else (87,87,87)
			# image from part
			im = self.parts_imgs[i]
			# position
			x, y = self.parts_pos
			x += (i%2)* int(self.width / 13.3)		# images in same line
			y += (i//2)* int(self.height / 7.15)	# images in same column
			# gray border
			w,h = self.parts_size	# part width, height
			d = 5					# border distance from image
			pygame.draw.rect(self.screen, color, (x-d,y-d, w+d*2,h+d*2), 2)
			# image blit
			self.screen.blit(im, (x, y) )
		# display selector
		x, y = self.parts_pos
		x -= int(self.width / 90)
		y -= int(self.height / 50)
		x += self.selector_j* int(self.width / 13.3)
		y += self.selector_i* int(self.height / 7.15)
		self.screen.blit(self.selector_img, (x, y) )
		# testing_inputs_rect
		if self.testing_inputs_rect != None:
			color, pos, size = self.testing_inputs_rect
			pygame.draw.rect(self.screen, color, pos, size)
			self.testing_inputs_rect = None
		# timer
		textsurface = self.myfont.render(str(self.timer), False, (250,100,100))
		self.screen.blit(textsurface, self.timer_pos)
		# screen update
		pygame.display.update()

	def timer_update(self):
		self.timer += 1
		self.display_update()

def main():
	game = Recreation()

	running = True
	while running:
	#  events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.USEREVENT+1:
				pygame.time.set_timer(pygame.USEREVENT+1, 0)
				game.start()
			if event.type == pygame.USEREVENT+2:
				game.timer_update()
			if event.type == pygame.KEYDOWN:
				# clear the input list
				if event.key == pygame.K_ESCAPE:
					game.clear_saved_inputs()
				# tab checks if input is right
				elif event.key == pygame.K_TAB:
					game.testing_inputs()
					game.clear_saved_inputs()
				elif event.key == pygame.K_g: # test
					print(pygame.mouse.get_pos())
				# append input to list
				else:
					k_name = pygame.key.name(event.key)
					game.move_selector(k_name)
				# screen update
				game.display_update()

main()
