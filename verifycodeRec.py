import os
from base64 import b64decode
from StringIO import StringIO
from PIL import Image


class ImageProcessHelper(object):
	@staticmethod
	def stub():
		print('stub')
		
	@staticmethod
	def saveAsJpeg(im, path):
		ImageProcessHelper.safeSave(im, path, 'jpeg')


	@staticmethod
	def saveAsBMP(im, path):
		ImageProcessHelper.safeSave(im, path, 'bmp')


	@staticmethod
	def safeSave(im, path, ext='bmp'):
		try:
			im.save(path, ext)
		except Exception as e:
			print(e)

	@staticmethod
	def save(im):
		im.save('codeout', 'jpeg')


	@staticmethod
	def noise(im):
		im = im.convert('L')
		im = im.point(lambda i: i > 141 and 255)
		return im	

	@staticmethod
	def crop(im):
		crops = []

		start_x = 8
		gap_x = 4
		width = 9	# or 10

		for i in range(0, 4):
			tmp = im.crop((start_x+gap_x*i+width*i, 0, start_x+gap_x*i+width*(i+1), 20))
			crops.append(tmp)

		return crops


	@staticmethod
	def removeBlank(im):
		def rev(p):
			if p == 255:
				return 0
			else:
				return 255

		rim = im.point(rev)
		return im.crop(rim.getbbox())


	@staticmethod
	def familiarity(im1, im2):
		if im1.mode != 'L':
			im1 = im1.convert('L')

		if im2.mode != 'L':
			im2 = im2.convert('L')

		w = min(im1.size[0], im2.size[0])
		h = min(im1.size[1], im2.size[1])
		# print('w:%d, h:%d' % (w, h))

		fa = 0
		for x in range(w):
			for y in range(h):
				if im1.getpixel((x, y)) ^ im2.getpixel((x, y)):
					pass
				else:
					fa+=1

		return fa


class Recognizer(object):

	def __init__(self, dir):
		self.prepare(dir)

	def prepare(self, dir):
		self.lib = []

		for _, _, paths in os.walk(dir):
			for path in paths:
				fileName = path.split('/')[-1]	# fileName is the code of img
				if fileName[0] == '.':
					continue
				self.lib.append((Image.open(dir+'/'+path), fileName))


	def recognize(self, fileName):
		im = None

		try:
			im = Image.open(fileName)
		except Exception as e:
			return
		
		im = ImageProcessHelper.noise(im)
		ims = ImageProcessHelper.crop(im)
		ims_noblank = []
		for iter_im in ims:
			ims_noblank.append(ImageProcessHelper.removeBlank(iter_im))

		ims = ims_noblank
		result = ''

		for iter_im in ims:
			fa = 0
			matchResult = []

			for template in self.lib:
				thisFa = ImageProcessHelper.familiarity(iter_im, template[0])
				if fa < thisFa:
					fa = thisFa
					matchResult = template

			print(matchResult)
			result += matchResult[1][0]

		# key step if u wantu see
		# im.save(result, 'bmp')
		return result

	def recognizeDir(self, dir):
		fileList = os.listdir(dir)
		for fileName in fileList:
			recognize(dir+'/'+fileName, self.lib)

	def recognizeData(self, data):
		im = None

		try:
			im = Image.open(StringIO(data))
		except Exception as e:
			print(e)
			return
		print(im)
		
		im = ImageProcessHelper.noise(im)
		ims = ImageProcessHelper.crop(im)
		ims_noblank = []
		for iter_im in ims:
			ims_noblank.append(ImageProcessHelper.removeBlank(iter_im))

		ims = ims_noblank
		result = ''

		for iter_im in ims:
			fa = 0
			matchResult = []

			for template in self.lib:
				thisFa = ImageProcessHelper.familiarity(iter_im, template[0])
				if fa < thisFa:
					fa = thisFa
					matchResult = template

			print(matchResult)
			result += matchResult[1][0]

		return result

	def recognizeB64(self, b64Data):
		data = None

		try:
			data = b64decode(b64Data)
		except Exception as e:
			return ''

		r = self.recognizeData(data)
		return r

# ---------------------------------

def gen(fileName):
	try:
		im = Image.open(fileName)
	except Exception as e:
		print(e)
		return

	im = im.convert('L')
	im = noise(im)
	ims = crop(im)

	ext = 'bmp'
	for i in range(0, len(ims)):
		fileName = fileName.split('/')[-1]
		removeBlank(ims[i]).save(fileName[i], ext)


def genDir(dir):
	for fileName in os.listdir(dir):
		learn(os.getcwd()+'/'+dir+'/'+fileName)


if __name__ == '__main__':
	# main()
	# learnDir('case1')
	# rec = Recognizer('template')
	# r = rec.recognize('code')
	# print(r)
	# recognizeDir('case3', lib)
	pass
