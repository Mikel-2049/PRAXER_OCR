from utils import is_similar

import pandas as pd
import cv2
from pytesseract import pytesseract as PT


PT.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def preprocess_image(img, coords):
    # Extract the region of interest using the coordinates
    x, y, w, h = coords
    cell = img[y:y+h, x:x+w]

    # Convert to grayscale
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    # Thresholding to get a binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Resize the image to make it larger for better OCR
    scale_factor = 2.5  # Example: Make the image double its size
    width = int(w * scale_factor)
    height = int(h * scale_factor)
    dim = (width, height)

    # Perform the actual resizing of the image
    resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_LINEAR)

    return resized


def read_tag(image_path, column, num_rows):
    img = cv2.imread(image_path)
    data = []

    for i, coords in enumerate(column):
        if i == 0:  # Skip the title cell after the check
            continue
        
        # Preprocess the image (including resizing) using the coordinates
        processed_cell = preprocess_image(img, coords)

        custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- --psm 6'

        text = PT.image_to_string(processed_cell, config=custom_config).strip()

        # Append the text to the data list
        data.append(text)

    df = pd.DataFrame(data, columns=['TAG'])
    #print(df)

    return df

