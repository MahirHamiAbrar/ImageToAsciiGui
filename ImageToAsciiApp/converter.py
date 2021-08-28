import sys
import random
import numpy as np

from PIL import Image

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale = '@%#*+=-:. '

# runtime function
runtime_evt_manager = None


# set runtime function
def setRuntimeEventManager(func):
    global runtime_evt_manager

    if callable(func):
        runtime_evt_manager = func

# set runtime function
def callRuntimeEventManager(data):
    global runtime_evt_manager

    if callable(runtime_evt_manager):
        runtime_evt_manager.__call__(data)

# get average luminance of image
def getAverageLuminance(image):
    """
     Given image, returns average value of grayscale value
    """
    # convert the image to grayscale array
    im = np.array(image)
    # get the image shape
    w, h = im.shape
    # return the average value of grayscale value
    return np.average(im.reshape(w*h))

# convert the image to ASCII
def convertImageToAscii(imageFile, cols, scale):
    """
     Given Image and dimensions (rows x cols); returns a 'm x n' list of ASCII text
    """

    global gscale


    data = {}

    # open the image and convert it to grayscale
    image = Image.open(imageFile).convert('L')

    img_size = image.size   # size of the image

    # extract width and height
    W, H = img_size[0], img_size[1]

    # calculate the width
    w = W/cols
    # calculate the height keeping based on ratio and scale
    h = w/scale

    # claculate the number of rows
    rows = int(H/h)

    # check if the image is too small, if yes, then exit
    if cols > W or rows > H:
        data['error'] = 'Image is too small to convert!'
        callRuntimeEventManager(data)
        sys.exit(0)
    else:
        data['img-dims'] = [W, H]
        data['tile-dims'] = [w, h]
        data['rows'] = rows
        data['cols'] = cols
        data['error'] = None

        callRuntimeEventManager(data)

    # declare a list for storing ascii characters
    ascii_img = []

    # start conversion
    for i in range(rows):
        y1 = int(i * h)
        y2 = int((i + 1) * h)

        # corretion of last tile
        if i == rows - 1:
            y2 = H

        # add an empty string to the list
        ascii_img.append("")

        for j in range(cols):
            x1 = int(j * w)
            x2 = int((j + 1) * w)

            # corretion of last tile
            if j == cols - 1:
                x2 = W

            # crop the image to the specified tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance of the image
            avgL = int(getAverageLuminance(img))

            # get the gray scale value
            gsVal = gscale[int((avgL * 9) / 255)]

            # add the ascii character to the list
            ascii_img[i] += gsVal

    # return the text image
    return ascii_img

# create the output text
def createOutputText(ascii_img):
    text_image = ""

    for row in ascii_img:
        # add a new line if the string isn't a blank line
        if text_image != "":
            text_image += "\n"

        # add row to the string
        text_image += row

    return text_image

# save the output file
def saveOutputFile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


# a test main function
def main():
    cols = 50
    scale = 0.43

    imgFile = 'C:/Users/USER/Pictures/LAEO_Logo/LEAO_v1_2.jpg'
    outFile = 'C:/Users/USER/Desktop/Image.txt'

    setRuntimeEventManager(print)

    # now convert the image to ascii
    ascii_img = convertImageToAscii(imgFile, cols, scale)
    # create the output text
    text = createOutputText(ascii_img)
    # save it
    saveOutputFile(outFile, text)

    # show it
    print(text)


# run the code
if __name__ == '__main__':
    main()
