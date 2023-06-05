import sys
from PIL import Image
from PIL import ImageChops


def encodeLSB(img, secret):
    img = Image.open(img_path).convert('RGB')
    # Convert the secret to binary
    secret_binary = ''.join(format(ord(i), '08b') for i in secret)
    # print("secretBinary:" + secretBinary)

    # Get the image szies
    width, height = img.size
    maxLength = width * height * 3 // 8

    # Check if the message is too long
    if len(secret_binary) > maxLength:
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
                if index < len(secret_binary):
                    # Get the least significant bit (LSB)
                    lsb = secret_binary[index]
                    # Encode the LSB into the pixel
                    pixel[i] = int(bin(pixel[i])[2:9] + lsb, 2)
                    index += 1

            # Save the pixel value
            img.putpixel((col, row), tuple(pixel))

    new_path = img_path.split('.')[0] + "_ssh." + img_path.split('.')[-1]
    img.save(new_path)
    print("Encoded image saved as \"" + new_path + "\".")
    # print("Encoded image saved as \"" + new_path + "\" with the message:\n" + secretMessage)

    return img, new_path


def encode(img_path, secret):
    img = Image.open(img_path).convert('RGB')
    # Convert the secret to binary
    secret_binary = ''.join(format(ord(i), '08b') for i in secret)
    # print("secretBinary:" + secretBinary)

    # Get the image szies
    width, height = img.size
    maxLength = width * height * 3 // 8

    # Check if the message is too long
    if len(secret_binary) > maxLength:
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
                if index < len(secret_binary):
                    # Get the least significant bit (LSB)
                    lsb = secret_binary[index]
                    # Encode the LSB into the pixel
                    pixel[i] = int(bin(pixel[i])[2:9] + lsb, 2)
                    index += 1

            # Save the pixel value
            img.putpixel((col, row), tuple(pixel))

    new_path = img_path.split('.')[0] + "_ssh." + img_path.split('.')[-1]
    img.save(new_path)
    print("Encoded image saved as \"" + new_path + "\".")
    # print("Encoded image saved as \"" + new_path + "\" with the message:\n" + secretMessage)

    return img, new_path


def compare_images(image_1_path, image_2_path):
    img1 = Image.open(image_1_path).convert('RGB')
    img2 = Image.open(image_2_path).convert('RGB')

    img_diff = ImageChops.difference(img1, img2)

    for x in range(img_diff.width):
        for y in range(img_diff.height):
            pixel = img_diff.getpixel((x, y))
            if pixel != (0, 0, 0):
                img_diff.putpixel((x, y), (0, 255, 0))

    img_diff.show()

    path_to_save = image_1_path.split('.')[0] + "_diff." + image_1_path.split('.')[-1]
    img_diff.save(path_to_save)
    print("Difference image saved as \"" + path_to_save + "\"")

    return img_diff, path_to_save


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python hide.py <image> <secret message> --diff(optional)")
        print("Necessities:")
        print("       <image>          : the image to hide the secret message in.")
        print("       <secret message> : the secret message to hide in the image.")
        print("Optional Arguments:")
        print("       --diff           : show the difference between the original image and the encoded image.")
        sys.exit(1)

    img_path = sys.argv[1]
    secretMessage = sys.argv[2]

    # Open the image with RGB mode
    img = Image.open(img_path).convert('RGB')

    # Get the maximum message length
    width, height = img.size
    maxLength = width * height * 3 // 8

    # Check if the message is too long
    if len(secretMessage) > maxLength:
        print("The message is too long!")
        sys.exit(1)

    # Encode the message
    img_encoded, img_encoded_path = encode(img_path, secretMessage)

    if sys.argv[3].__eq__("--diff"):
        compare_images(img_path, img_encoded_path)
