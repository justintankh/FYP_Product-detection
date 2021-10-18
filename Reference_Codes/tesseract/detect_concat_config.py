import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
from os.path import exists
import os

# get grayscale image


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal


def remove_noise(image):
    return cv2.medianBlur(image, 5)

# thresholding


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# dilation


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

# erosion


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

# opening - erosion followed by dilation


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection


def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching


def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# Preparing output directory
k = 0
input_file = './input/cookingcream1_out.jpg'
output_dir = f'./output/experiment_{k}'
while (exists(output_dir)):
    k += 1
    output_dir = f'./output/experiment_{k}'
os.mkdir(output_dir)

# Plot original image
image = cv2.imread(input_file)
b, g, r = cv2.split(image)
rgb_img = cv2.merge([r, g, b])

# Preprocess image
gray = get_grayscale(image)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
images = {'gray': gray,
          'thresh': thresh,
          'opening': opening,
          'canny': canny}


# Refresh cv2image
cv2image = cv2.imread(input_file)
# Set OEM, PSM and Blacklist
psmConfig = ['11', '6', '11']
filterConfig = ['opening', 'thresh', 'thresh']
psmUsed = '+'.join(psmConfig)
filterUsed = '+'.join(filterConfig)
wordsDetected = []
prevCoords = []
# Detect for the following pre-processing filters, results linearly concated
for filter, psm in zip(filterConfig, psmConfig):
    custom_config = f'--oem 3 --psm {psm} -l eng -c tessedit_char_blacklist=!@#$%^&*()_-+=\|/?><—'
    readImage = images[filter]

    try:
        results = pytesseract.image_to_data(
            readImage, output_type=Output.DICT, config=custom_config)
        # print(custom_config)
    except:
        print(f'${custom_config} error')
        continue

    for i in range(0, len(results["text"])):
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        text = results["text"][i]
        conf = float(str(results["conf"][i])[:4])
        if len(text) <= 2 or '—' in text:
            continue

        if conf > 60:
            # Check for duplicate OCR
            exitKey = False
            for coords in prevCoords:
                x_diff = x - coords[0]
                y_diff = y - coords[1]
                w_diff = w - coords[2]
                h_diff = h - coords[3]

                # print(f'Same text - \n{abs(x_diff)} {abs(y_diff)}\n')

                if (abs(x_diff) < 40 and abs(y_diff) < 40):
                    print(
                        f'Same text - {text}\n{x_diff} {y_diff} {w_diff} {h_diff}\n')
                    exitKey = True
            # Skip result if duplicate detected
            if(exitKey):
                continue

            # Store coordinate and words
            prevCoords.append([x, y, w, h])
            wordsDetected.append(text)
            print(wordsDetected)

            # Write coordinate
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(cv2image, text, (x + 50, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (79, 255, 255), 2)
            cv2.putText(cv2image, str(conf)[
                        :2], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.destroyAllWindows()
cv2.imshow('cv2image', cv2image)
cv2.waitKey(1)
cv2.imwrite(f'{output_dir}/{filterUsed}_oem3_psm{psmUsed}.png', cv2image)
print(f'saved at {output_dir}/{filterUsed}_oem3_psm{psmUsed}.png')

# Get OCR output using Pytesseract
# print('-----------------------------------------')
# print('TESSERACT OUTPUT --> ORIGINAL IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(image, config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> GREY IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images['gray'], config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> THRESHOLDED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images['thresh'], config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> OPENED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images['opening'], config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> CANNY EDGE IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images['canny'], config=custom_config))
