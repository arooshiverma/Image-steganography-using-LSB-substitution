import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random

img_name = "Cover_1.png"
img = None
stego = None
def getBit(n, i):
	if((n>>i)%2 == 1):
		return 1
	return 0

def setP(nc00,c00,nc01,c01,nc10,c10,nc11,c11):
	p = "";
	if(nc00>c00):
		p = "1"
	else:
		p = "0"
	if(nc01>c01):
		p = p+"1"
	else:
		p = p+"0"
	if(nc10>c10):
		p = p+"1"
	else:
		p = p+"0"
	if(nc11>c11):
		p = p+"1"
	else:
		p = p+"0"

	return p

def createSecretKey(l):
	s = ""
	while(l>=0):
		x = str(random.randint(0, 1))
		s = s+x
		l = l-1

	f = open("A17CS02006_key_gray.txt", "w")
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
	l = img.shape[0]
	r = img.shape[1]
	klen = len(key);

	mlen = len(msg)
	print("Length of message is:", mlen)
	mx = str(bin(mlen))[2:]
	mx = ("0"*(17-len(mx))) + mx
	#print(mx)
	msg = mx + msg
	mlen = len(msg)

	tc = 0
	for i in range(l):
		for j in range(r):
			x = key[(i*r + j)%klen]
			x = int(x)
			x = x<<1
			#print(x, img[i][j], (x^img[i][j]))
			if(((x^img[i][j])>>1)%2 == 1):
				tc = tc+1


	if(mlen > tc-4):
		print("Message too big for optimized encryption.")
		return 0

	#print("Here")
	i = 0
	j = 4
	cnt = 0
	stego = img
	c00=0
	c01=0
	c11=0
	c10=0
	nc00=0
	nc11=0
	nc01=0
	nc10=0
	while(i<l and cnt<mlen):
		j = 0
		if(i == 0):
			j = 4
		while(j<r and cnt<mlen):
			x = int(key[(i*r + j)%klen])
			x = x<<1
			mbit = int(msg[cnt])
			mbit = 2**8 - 2 + mbit
			if(getBit(x^img[i][j], 1)):
				stego[i][j] = ((img[i][j] | np.uint64(1)) & np.uint64(mbit))
				if(getBit(img[i][j], 1)==0 and getBit(img[i][j], 2)==0):
					if(getBit(img[i][j], 0) == getBit(stego[i][j], 0)):
						c00 = c00 + 1;
					else:
						nc00 = nc00+1;
				elif(getBit(img[i][j], 1)==0 and getBit(img[i][j], 2)==1):
					if(getBit(img[i][j], 0) == getBit(stego[i][j], 0)):
						c01 = c01+1;
					else:
						nc01 = nc01+1;

				elif(getBit(img[i][j], 1)==1 and getBit(img[i][j], 2)==0):
					if(getBit(img[i][j], 0) == getBit(stego[i][j], 0)):
						c10 = c10 + 1;
					else:
						nc10 = nc10+1;

				else:
					if(getBit(img[i][j], 0) == getBit(stego[i][j], 0)):
						c11 = c11 + 1;
					else:
						nc11 = nc11+1;
				cnt = cnt + 1
			j = j+1
		i = i+1
	if(cnt < mlen):
		return 0
	#print("Here")

	#Setting value of p
	p = setP(nc00,c00,nc01,c01,nc10,c10,nc11,c11)
	for i in range(4):
		mbit = int(p[i])
		mbit = 2**8 - 2 + mbit
		stego[0][i] = ((stego[0][i] | np.uint64(1)) & np.uint64(mbit))

	#inverting
	i=0
	cnt = 0
	while(i<l and cnt<mlen):
		j=0
		if(i==0):
			j = 4
		while(j<r and cnt<mlen):
			x = int(key[(i*r + j)%klen])
			x = x<<1
			if(getBit(x^img[i][j], 1)):
				cnt=cnt+1
				if(getBit(img[i][j], 1)==0 and getBit(img[i][j], 2)==0 and nc00>c00):
					if(getBit(stego[i][j], 0) == 1):
						stego[i][j] = stego[i][j] & (stego[i][j]-1)
					else:
						stego[i][j] = stego[i][j] | 1

				elif(getBit(img[i][j], 1)==0 and getBit(img[i][j], 2)==1 and nc01>c01):
					if(getBit(stego[i][j], 0) == 1):
						stego[i][j] = stego[i][j] & (stego[i][j]-1)
					else:
						stego[i][j] = stego[i][j] | 1

				elif(getBit(img[i][j], 1)==1 and getBit(img[i][j], 2)==0 and nc10>c10):
						if(getBit(stego[i][j], 0) == 1):
							stego[i][j] = stego[i][j] & (stego[i][j]-1)
						else:
							stego[i][j] = stego[i][j] | 1

				elif(getBit(img[i][j], 1)==1 and getBit(img[i][j], 2)==1 and nc11>c11):
						if(getBit(stego[i][j], 0) == 1):
							stego[i][j] = stego[i][j] & (stego[i][j]-1)
						else:
							stego[i][j] = stego[i][j] | 1
			j = j+1
		i = i+1


	cv.imshow('Encrypted Image', stego)
	cv.imwrite('Encrypted_'+img_name, stego)

	#print(p, msg, mlen)
	#print(img)
	return 1


if __name__ == "__main__":
	print("Using image " + img_name)

	img =  cv.imread(img_name) 
	#print(img)
	#print(img.shape)
	cv.imshow('Original image', img)
	plt.imshow(img)

	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	#print(gray)
	#print(gray.shape)
	cv.imshow('Gray scaled image', gray)
	plt.imshow(img)

	l = gray.shape[0]
	r = gray.shape[1]
	#print(l,r)
	key = createSecretKey(l*r)
	#key = "1100111111101100"

	print("Enter secret text: ")
	msg = input()

	bin_msg = convertMsgToBin(msg)
	#print(bin_msg)

	print()
	flag = stegan(gray, key, bin_msg)
	if(flag == 0):
		print("Encryption failed :(")
	else:
		print("Encryption successful! :D")
		original = cv.imread(img_name) 
		changed = cv.imread('Encrypted_'+img_name) 
		psnr = cv.PSNR(original, changed)
		print("PSNR value is: ", psnr)

			
	cv.waitKey()
