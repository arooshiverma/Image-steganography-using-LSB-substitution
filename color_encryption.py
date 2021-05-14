import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random

#FIrst 16 bits is msg size
img_name = "Cover_2.png"
def createSecretKey(l):

	s = ""
	while(l>=0):
		x = str(random.randint(0, 1))
		s = s+x
		l = l-1

	#s = "1111111111111"
	f = open("key_color.txt", "w")
	f.write(s)
	f.close()

	return s;

def convertMsgToBin(m):
	res = ''
	for i in m:
		x = str(format(ord(i), 'b'))
		x = ('0'*(8-len(x)))+x
		res = res+x
	return res

def stegan(img, key, msg):

	#If xor is 1 then Green, otherwise Blue

	l = img.shape[0]
	r = img.shape[1]
	klen = len(key);

	mlen = len(msg)
	print("Length of message is:", mlen)
	mx = str(bin(mlen))[2:]
	mx = ("0"*(16-len(mx))) + mx
	#print(mlen)
	msg = mx + msg
	mlen = len(msg)
	#print(mlen)
	#print(mx, msg)
	#print(l*r)
	#print(msg)
	#print(mlen)
	if(mlen > l*r):
		print("Message too big for encryption")
		return 0

	i = 0
	j = 0
	f = 1
	while(i<l and f == 1):
		j = 0
		while(j<r and f == 1):
			#print(i, j)
			x = key[(i*r + j)%klen]
			x = int(x)
			mbit = int(msg[i*r+j])
			mbit = 2**8 - 2 + mbit
			if((x^img[i][j][0])%2 == 1):
				img[i][j][1] = ((img[i][j][1] | np.uint64(1)) & np.uint64(mbit))
			else:
				img[i][j][2] = ((img[i][j][2] | np.uint64(1)) & np.uint64(mbit))
			j = j+1;
			if(i*r+j >= mlen):
				f = 0
		i=i+1;

	cv.imshow('Encrypted Image', img)
	cv.imwrite('Encrypted_'+img_name, img)

	#print(img)
	return 1


if __name__ == "__main__":
	
	
	print("Using image " + img_name)

	img =  cv.imread(img_name) 
	#print(img)
	#print(img.shape)
	l = img.shape[0]
	r = img.shape[1]

	key = createSecretKey(l*r)
	


	#Show original image
	cv.imshow('Original image', img)
	plt.imshow(img)

	print("Enter secret text: ")
	msg = input()
	#print(secret)

	bin_msg = convertMsgToBin(msg)
	#print(bin_msg)
	#print(img)
	#print()
	#print()
	flag = stegan(img, key, bin_msg)
	if(flag == 0):
		print("Encryption failed :(")
	else:
		print("Encryption successful! :D")

	original = cv.imread(img_name) 
	changed = cv.imread('Encrypted_'+img_name) 
	psnr = cv.PSNR(original, changed)
	print("PSNR value is: ", psnr)

	cv.waitKey()

	



	



