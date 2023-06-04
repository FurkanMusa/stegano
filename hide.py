import sys
from PIL import Image


def encode(img, secret):
    # Hide the secret into img
    # Convert the secret to binary
    secretBinary = ''.join(format(ord(i), '08b') for i in secret)
    # Get the image width and height
    width, height = img.size
    # Get the maximum message length
    maxLength = width * height * 3 // 8
    # Check if the message is too long
    if len(secretBinary) > maxLength:
        print("The message is too long!")
        sys.exit(1)
    # Encode the secret into the image
    index = 0
    for row in range(height):
        for col in range(width):
            # Get the pixel value
            pixel = list(img.getpixel((col, row)))
            # Encode the secret into the pixel value
            for i in range(0, 3):
                if index < len(secretBinary):
                    # Get the least significant bit (LSB)
                    lsb = secretBinary[index]
                    # Encode the LSB into the pixel
                    pixel[i] = int(bin(pixel[i])[2:9] + lsb, 2)
                    index += 1
            # Save the pixel value
            img.putpixel((col, row), tuple(pixel))
    return img


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python hide.py <image> <secret message>")
        sys.exit(1)

    imgBase = sys.argv[1]
    secretMessage = sys.argv[2]

    # Open the image with RGB mode
    img = Image.open(imgBase).convert('RGB')

    # Get the maximum message length
    width, height = img.size
    maxLength = width * height * 3 // 8

    # Check if the message is too long
    if len(secretMessage) > maxLength:
        print("The message is too long!")
        sys.exit(1)

    # Encode the message
    imgEncoded = encode(img, secretMessage)

    # Save the output image with the same name as the input image and "s" prefix
    imgEncoded.save("Shh" + imgBase)
    print("Encoded image saved as \"Shh" + imgBase + "\" with the message:\n" + secretMessage)
