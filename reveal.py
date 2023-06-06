import sys
from PIL import Image
from mpmath import mp

from hide import stash_to_pixel, pixel_to_stash


# Decode the secret message from encoded image
def decodeLSB(imgEncoded):
    # Get the image width and height
    width, height = imgEncoded.size
    # Decode the secret from the image
    index = 0
    secretBinary = ""
    for row in range(height):
        for col in range(width):
            # Get the pixel value
            pixel = list(imgEncoded.getpixel((col, row)))
            # Decode the secret from the pixel value
            for i in range(0, 3):
                # Get the least significant bit (LSB)
                lsb = bin(pixel[i])[-1]
                # Decode the LSB from the pixel
                secretBinary += lsb
                index += 1

    # Convert the binary to string
    secret = ""
    for i in range(0, len(secretBinary), 8):
        # Get the character from binary
        char = chr(int(secretBinary[i:i + 8], 2))
        # Check if the character is null
        if char == '\0':
            break
        # Save the character
        secret += char
    return secret


def decode(img_path):
    img = Image.open(img_path).convert('RGB')

    width, height = img.size
    total_stash = width * height * 3 // 100

    print("Total stash: " + str(total_stash))
    total_stash = 80
    mp.dps = total_stash + 20  # set number of digits of pi
    pi = str(mp.pi)
    print(pi)

    # Encode the secret into the image
    index = 0
    stash = 0
    pi_step = 2
    secret_binary = ""
    for i in range(total_stash):
        while int(pi[pi_step]) == 0:
            print("skip zero")
            pi_step += 1
        stash = stash + int(pi[pi_step])

        x, y, rgb = stash_to_pixel(width, height, stash)

        # Get the pixel value
        pixel = list(img.getpixel((x, y)))

        # Get LSB
        lsb = bin(pixel[rgb])[-1]

        # Decode the LSB from the pixel
        secret_binary += lsb

        print("i, pi_step, BIN: " + str(i) + ", " + pi[pi_step] + ", " + secret_binary[index] +
              " \t| stash >< (x,y)[RGB]: " + str(stash) + " >< (" + str(x) + ", " + str(y) + ")[" + str(rgb) + "]  " +
              " \t| " + secret_binary[i])

        pi_step += 1
        index += 1

    # Convert the binary to string
    secret = ""
    for i in range(0, len(secret_binary), 8):
        # Get the character from binary
        char = chr(int(secret_binary[i:i + 8], 2))
        # Check if the character is null
        if char == '\0':
            break
        # Save the character
        secret += char
    return secret


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("ERROR: Invalid arguments!")
        print("Usage: python reveal.py <image with secrets>")
        print("Necessities:")
        print("       <image with secrets>: the image reveal secrets from.")
        sys.exit(1)

    img_path = sys.argv[1]

    print("Hidden message was:\n" + decode(img_path))
