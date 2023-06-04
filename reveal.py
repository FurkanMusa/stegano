import sys
from PIL import Image


def decode(imgEncoded):
    # Decode the secret message from encoded image
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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python reveal.py <image with secrets>")
        sys.exit(1)

    imgBase = sys.argv[1]

    imgEncoded = Image.open(imgBase).convert('RGB')

    print("Hidden message was:\n" + decode(imgEncoded))
