import cv2
import os
# from PIL import Image
import numpy as np
# from multiprocessing import Pool
from threading import Thread
import time

# def list(root, pathSet, select = 'jpg'):
# 	for path in os.listdir(root):
# 		ori_path = os.path.join(root,path)
# 		if (os.path.isdir(ori_path)):
# 			list(ori_path, pathSet, select)
# 		elif (os.path.isfile(ori_path)):
# 			if path.split('.')[-1] == select:
# 				pathSet.append(ori_path)
# 			else:
# 				print('Not an image.')

# root = 'C:\\Users\\USER-WNB\\Desktop\\datasets\\illust'
# pathSet = []
# list(root, pathSet, select = 'jpg')
# print(pathSet)

def list_dir(root):
	dir = []
	for path in os.listdir(root):
		ori_path = os.path.join(root, path)
		if os.path.isdir(ori_path):
			dir.append(ori_path)
	return dir

def list_file(root, select = 'jpg'):
	pathName = []
	notImage = 0
	for path in os.listdir(root):
		oriPath = os.path.join(root, path)
		if os.path.isfile(oriPath):
			if oriPath.split('.')[-1] == select:
				pathName.append(oriPath)
			else:
				notImage += 1
	print("There are {} files not image.".format(notImage))
	return pathName

def sketch(ori, blur, threshold = 8):
	t1, t2 = ori.reshape((512*512)), blur.reshape((512*512))
	print(t1.shape)
	tmp = [0 if y1 <= 20 or (y1 + threshold) < y2 else 255 for y1,y2 in zip(t1, t2)]
	return np.array(tmp).reshape((512,512))

def gray_sketch(ori, blur, threshold = 8):
	t1, t2 = ori.reshape((512*512)), blur.reshape((512*512))
	print(t1.shape)
	tmp = []
	for y1,y2 in zip(t1, t2):
		if y1 <= 20:
			tmp.append(0)
		elif y1 + threshold < y2:
			tmp.append(y1)
		else:
			tmp.append(255)
	return np.array(tmp).reshape((512,512))

def run():
	start = time.time()
	root = 'C:\\Users\\USER-WNB\\your_image_path'
	save = 'C:\\Users\\USER-WNB\\sketch_save_path'
	for path in dict.fromkeys(list_dir(root),True):
		pathName = dict.fromkeys(list_file(path), True)
		if not os.path.isdir(os.path.join(save, path.split('\\')[-1])):
			os.mkdir(os.path.join(save, path.split('\\')[-1]))

		for name in pathName:
			img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
			blur = cv2.GaussianBlur(img,(11,11),0)
			tmp = sketch(img, blur)
			cv2.imwrite(os.path.join(save, name.split('\\')[-2], name.split('\\')[-1]), tmp)

	end = time.time()
	print(end - start)

def mul_run(threadNum = 4):
	start = time.time()
	filterSize = 11
	root = 'C:\\Users\\USER-WNB\\your_image_path'
	save = 'C:\\Users\\USER-WNB\\sketch_save_path'
	
	
	for path in dict.fromkeys(list_dir(root),True):
		pathName = dict.fromkeys(list_file(path), True)
		if not os.path.isdir(os.path.join(save, path.split('\\')[-1])):
			os.mkdir(os.path.join(save, path.split('\\')[-1]))

		threads = []
		count = 1
		for name in pathName:
			count += 1
			t = Thread(target=mul_sketch, args=(name, save, filterSize, ))
			t.start()
			threads.append(t)
			if count > threadNum:
				count = 1
				for t in threads:
					t.join()	
				threads = []	


	end = time.time()
	print(end - start)

def mul_sketch(name, save, filterSize = 11):
	# save = 'C:\\Users\\USER-WNB\\Desktop\\datasets\\sketch\\danbooru-images'
	img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	blur = cv2.GaussianBlur(img,(filterSize, filterSize),0)
	# tmp = sketch(img, blur)
	tmp = gray_sketch(img, blur)
	cv2.imwrite(os.path.join(save, name.split('\\')[-2], name.split('\\')[-1]), tmp)

# def image_read(path):
# 	# f = open(path, 'rb')
# 	# img = Image.open(f)
# 	img = Image.open(path)
# 	# img.save('test/' + path.split('\\')[-1])
# 	# f.close()
# 	return img



# start = time.time()
# root = 'C:\\Users\\USER-WNB\\Desktop\\datasets\\illust\\danbooru-images'
# for path in dict.fromkeys(list_dir(root),True):
# 	pathName = dict.fromkeys(list_file(path), True)
	
# 	for name in pathName:
# 		# image_read(name)
# 		Image.open(name)
# end = time.time()
# print(end - start)

if __name__ =='__main__':
	# img = cv2.imread('2215000.jpg', cv2.IMREAD_GRAYSCALE)
	# blur = cv2.GaussianBlur(img,(5,5),90)
	# # cv2.imwrite('blur.jpg', blur)
	# cv2.imwrite('gray.jpg', img)
	# threshold = 8
	# # t1, t2 = img.reshape((512*512)), blur.reshape((512*512))
	# # tmp = [0 if y1 == 0 or (y1 + threshold) <= y2 else 255 for y1,y2 in zip(t1, t2)]
	# tmp = sketch(img, blur, threshold)
	# # tmp = np.array(tmp).reshape((512,512))
	# cv2.imwrite('tmp.jpg', tmp)
	# run()
	mul_run(100)
