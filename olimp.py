from PIL import Image
from threading import Thread
from threading import RLock
from queue import Queue
 
image = Image.open('C:\\Python\\Program\\img1.jpg')
(width, height) = image.size
dct = {}
cnt_thread = 2

lock = RLock()
q = Queue()
#old_percent = 0

def print_image():

	for key in dct.keys():
		if sum(dct[key]) > 100: image.putpixel(key, dct[key])
		else: image.putpixel(key, (0, 0, 0))

	image.show()

def filter(start_x, end_x):
	global dct

	for x in range(start_x, end_x):
		for y in range(height):

			if x == 0 or x == width - 1 or y == 0 or y == height - 1:
				dct[(x, y)] = (0, 0, 0)
				continue

			new_red, new_green, new_blue = 0, 0, 0
			for i in range(-1, 2):
				for j in range(-1, 2):
					if i != 0 or j != 0: 

						with lock:
							red, green, blue = image.getpixel((x + i, y + j))

						new_red += red
						new_green += green
						new_blue += blue

			with lock:
				red, green, blue = image.getpixel((x, y))
				dct[(x, y)] = (8*red - new_red, 8*green - new_green, 8*blue - new_blue)

			# percent = ((x*height + y) * 100) // (width * height)
			# if percent != old_percent:
			# 	print(str(percent) + "%")
			# 	old_percent = percent


if __name__ == '__main__':
	# th1 = Thread(target = filter, args = (0, ))
	# th2 = Thread(target = filter, args = (1, ))
	# th1.start()
	# th2.start()

	# q.join()

	filter(0, width//2)
	print_image()
