import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random

img_name = "Cover_2.png"
encrypted_img_name = "Encrypted_" + img_name

def getKey():
	f = open("A17CS02006_key_color.txt", "r")
	k = f.read()
	f.close()
	return k

def decrypt(img, key):
	l = img.shape[0]
	r = img.shape[1]
	klen = len(key)

	tot_msg = "";
	for i in range(l):
		for j in range(r):
			x = key[(i*r + j)%klen]
			x = int(x)
			if((x^img[i][j][0])%2 == 1):
				tot_msg = tot_msg + str(img[i][j][1] & np.uint64(1))
			else:
				tot_msg = tot_msg + str(img[i][j][2] & np.uint64(1))

	mlen = tot_msg[:16]
	mlen = "0b" + mlen
	mlen = int(mlen, 2)
	#print(mlen)
	msg = tot_msg[16:]
	msg = msg[:mlen]
	#print(msg, len(msg))
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
	

	key = getKey()

	msg = decrypt(img, key)

	print("The decrypted message is :", msg)


	
