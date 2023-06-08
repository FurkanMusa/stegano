# Pythyon Steganography 

This approach uses the least significant bit of some selected pixels to store a bit of the secret message.
This means that the image will be slightly altered, but the human eye will not be able to notice the difference.

The pixels that store the secret message are selected by a stepping value, which is the number of pixels that will be skipped before the next pixel is selected.
This stepping value is selected as next value of pi.

Pi is "3.14159...". So the first stepping value will be 1, the second 4, the third 1, the fourth 5, and so on.

---

**Installation:**
- pip install pillow
- pip install mpmath

---


To **hide** messages into a png image: \
> Usage: python hide.py \<image> \<secret message> --diff(optional)
> 
> Necessities:
> - \<image>          : the image to hide the secret message in.
> - \<secret message> : the secret message to hide in the image.
> 
> Optional Arguments:
> - --diff           : show the difference between the original image and the encoded image.
  
To **reveal** messages from an encoded png file: \
> Usage: python reveal.py \<image with secrets>
> 
> Necessities:
> - \<image with secrets>: the image reveal secrets from.
  
