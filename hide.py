import sys
from PIL import Image
from PIL import ImageChops


def encodeLSB(img, secret):
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


def encode(img, secret):
    # Convert the secret to binary
    secretBinary = ''.join(format(ord(i), '08b') for i in secret)
    # print("secretBinary:" + secretBinary)

    # Get the image szies
    width, height = img.size
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


def compareImgs(img1, img2):
    imgDiff = ImageChops.difference(img1, img2)
    imgDiff.show()
    return imgDiff


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python hide.py <image> <secret message> --diff(optional)")
        print("Necessities:")
        print("       <image>          : the image to hide the secret message in.")
        print("       <secret message> : the secret message to hide in the image.")
        print("Optional Arguments:")
        print("       --diff           : show the difference between the original image and the encoded image.")
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

    if sys.argv[3].__eq__("--diff"):
        img = Image.open(imgBase).convert('RGB')
        imgEncoded = Image.open("Shh" + imgBase).convert('RGB')
        imgDiff = compareImgs(img, imgEncoded)
        imgDiff.save("diff" + imgBase)
        print("diff image saved as \"diff" + imgBase + "\"")

