# Image-steganography-using-LSB-substitution
For grayscale images use 'gray_encryption.py' for hiding and 'gray_decryption.py' for decoding. The cover image name must be named "Cover_1.png".\
For RGB images use 'color_encryption.py' for hiding and 'color_decryption.py' for decoding. The cover image name must be named "Cover_2.png".

## Grayscale image steganography
The algorithm is taken from the paper 'A Secure Robust Gray Scale Image Steganography Using Image Segmentation'\
The algorithm is as follows:\
![Encryption Algorithm for grayscale Images](https://github.com/arooshiverma/Image-steganography-using-LSB-substitution/blob/main/gray1.JPG?raw=true)

Now, let us expand how the Steganography algorithm works for ith bit:
1. l = number of rows, r = number of columns, klen = key length
2. Let x = 2nd LSB of C(i, j), where C(i, j) is the element on ith row and jth column of the cover image.
3. Let mbit = M(cnt) {i.e. cntth bit of message}. Let k = K(i, j), i.e. the respective bit from key K. k can be calculated as:
k = key[(i*r + j)%klen]
4. if(x^k = 1) then
a) Change LSB of that image element
b) Increase cnt by 1
c) Check the 2nd and 3rd LSB of the Cover image pixel. Let g = string(2nd LSB) + string(3rd LSB), where ‘+’ is concatenation operator. Possible g values are {00, 01, 10, 11}
d) If the LSB of the pixel was changed in the step 4a, then increase the change-count of that particular g-type. Else increase the not-changed-count by 1.
For example if g=00 and LSB was changed from 0 to 1, then nc00 = nc00+1. If LSB wasn’t changed, c00 = c00+1
5. Move to the inversion algorithm part.

Let us move on to the inversion algorithm:
1. For each pixel S(i, j) of the stego-image:
a) Check the 2nd and 3rd LSB of the Cover image pixel. Let g = string(2nd LSB) + string(3rd LSB), where ‘+’ is concatenation operator. Possible g values are {00, 01, 10, 11}
b) If the changed-count>not-changed-count for that particular g, invert the LSB of that pixel.
For example: if g = 00, nc00 = 200 and c00=250, LSB = 0 then invert the LSB from 0 to 1.
2. Compute p. p is embedded in the LSBs of the first 4 pixels. It signifies whether inversion is done or not for the four categories of g: {00, 01, 10, 11}.
p[0] = (nc00>c00)
p[1] = (nc01>c01)
p[2] = (nc10>c10)
p[3] = (nc11>c11)

The DECRYPTION ALGORITHM is as follows:
1. Concatenate the LSBs of the first 4 pixels to form p.
2. Initialize msg = “”
3. Then loop over all pixels except the first 4 :
a. Let x = 2nd LSB of S(i, j), where C(i, j) is the element on ith row and jth column of the cover image.
b. Let k = K(i, j), i.e. the respective bit from key K. k can be calculated as:
k = key[(i*r + j)%klen]
c. if(x^k = 1) then:
i. msg = msg + getData(S(I, j), p).
ii. Here, the getData(pixel_val,p) function extracts the appropriate bit from the pixel. We compute g as we did in the encryption algorithm, then either invert the LSB(if the respective bit in p=1) or return the LSB as it is(otherwise).
4. We then extract the first 17 bits of msg, convert it from binary to decimal, and get the size of the secret message.
mlen = msg[0:17]
mlen = int(mlen)
5. Now we extract the required bits from msg (size = mlen)
msg = msg[17:17+mlen]
6. Finally, we convert the message from binary to ASCII

#### PSNR Values after embedding
![PSNR grayscale](https://github.com/arooshiverma/Image-steganography-using-LSB-substitution/blob/main/psnr1.JPG?raw=true)

## RGB image steganography
The algorithm is taken from the paper 'A Steganography Algorithm for Hiding Secret Message inside Image using Random Key'.

Encryption Algorithm:
![Encryption Algorithm for color Images](https://github.com/arooshiverma/Image-steganography-using-LSB-substitution/blob/main/enc.JPG?raw=true)

Decryption Algorithm:
![Encryption Algorithm for grayscale Images](https://github.com/arooshiverma/Image-steganography-using-LSB-substitution/blob/main/enc2.JPG?raw=true)
#### PSNR Values after embedding
![PSNR grayscale](https://github.com/arooshiverma/Image-steganography-using-LSB-substitution/blob/main/psnr2.JPG?raw=true)
