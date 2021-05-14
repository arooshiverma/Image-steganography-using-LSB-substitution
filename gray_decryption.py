import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random

img_name = "Cover_1.png"
encrypted_img_name = "Encrypted_" + img_name

def getBit(n, i):
	if((n>>i)%2 == 1):
		return 1
	return 0


def getKey():
	f = open("key_gray.txt", "r")
	k = f.read()
	f.close()
	return k

def getInv(n):
	if(n == 1):
		return 0
	return 1

def getData(p, n):
	#print(p, n,getBit(n, 1), getBit(n, 2), getBit(n, 0))
	if(getBit(n, 1)==0 and getBit(n, 2)==0):	
		if(p[0]=="1"):
			return getInv(getBit(n, 0))
		else:
			#print("a")
			return getBit(n, 0)

	if(getBit(n, 1)==0 and getBit(n, 2)==1):		
		if(p[1]=='1'):			
			return getInv(getBit(n, 0))
		else:
			#print("b")
			return getBit(n, 0)

	if(getBit(n, 1)==1 and getBit(n, 2)==0):		
		if(p[2]=='1'):			
			return getInv(getBit(n, 0))
		else:
			#print("c")
			return getBit(n, 0)

	if(getBit(n, 1)==1 and getBit(n, 2)==1):		
		if(p[3]=='1'):			
			return getInv(getBit(n, 0))
		else:
			#print("d")
			return getBit(n, 0)


def decrypt(img, key):
	l = img.shape[0]
	r = img.shape[1]
	klen = len(key)

	p = "";
	for j in range(4):
		x = key[(j)%klen]
		x = int(x)
		x = x<<1
		p = p + str(img[0][j] & np.uint64(1))
	#print("p", p)
	cnt = 0
	i,j = 0, 4
	tot_msg = ''
	xc = 0
	while(i<l):
		j=0
		if(i == 0):
			j=4

		while(j<r):
			x = int(key[(i*r + j)%klen])
			x = x<<1
			if(getBit(x^img[i][j], 1)==1):
				xc = xc+1
				tot_msg = tot_msg + str(getData(p, img[i][j]))
			j = j+1
		i = i+1
	#print("xc", xc)
	#print(tot_msg)
	mlen = '0b'+tot_msg[:17]
	mlen = int(mlen, 2)
	#print(mlen)
	#print(len(tot_msg))
	msg = tot_msg[17:17+mlen]

	val = len(msg)//8
	chunks, chunk_size = len(msg), len(msg)//val
	new_string = [ msg[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
	dec_msg = ''
	for i in new_string:
		#print(i)
		dec_msg += chr(int(i, 2))
	return dec_msg

if __name__ == "__main__":
	
	print("Using image " + encrypted_img_name)

	img =  cv.imread(encrypted_img_name) 
	#print(img)
	#print(img.shape)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	

	key = getKey()

	msg = decrypt(img, key)

	print("The decrypted message is :", msg)