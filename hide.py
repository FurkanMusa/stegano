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
    # Compare two images and paint different pixels black
    # Get the image sizes
    width, height = img1.size

    # Create a new image
    imgDiff = Image.new('RGB', (width, height), color='white')

    # Create a new pink pixel
    pink = (255, 0, 255)

    # Compare the images
    for row in range(height):
        for col in range(width):
            # Get the pixel values
            pixel1 = img1.getpixel((col, row))
            pixel2 = img2.getpixel((col, row))

            print("pixel1:" + str(pixel1))
            print("pixel2:" + str(pixel2))

            # Compare the pixels
            if pixel1 != pixel2:
                print("Different pixel found at (" + str(col) + ", " + str(row) + ")")
                imgDiff.putpixel((col, row), pink)

    return imgDiff


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

    # diff = ImageChops.difference(img, imgEncoded)
    # diff.save("diff" + imgBase)
    # print("diff image saved as \"diff" + imgBase + "\"")
