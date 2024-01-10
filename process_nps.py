from utils import is_similar

import pandas as pd
import cv2
from pytesseract import pytesseract as PT
import numpy as np


PT.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def preprocess_image(img, coords):
    x, y, w, h = coords
    cell = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    # Resize the image for better OCR
    scale_factor = 2.5
    resized_gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # Adaptive thresholding with a larger block size and a fine-tuned C value
    block_size = 41  # Block size for the adaptive threshold (try to keep it odd)
    C = 5  # Constant subtracted from the mean or weighted mean (this may need tuning)
    binarized = cv2.adaptiveThreshold(resized_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, block_size, C)

    return binarized




def read_nps(image_path, column, num_rows):
    img = cv2.imread(image_path)
    data = []
    
    # Ensure the first cell is what you expect, but do not add to data
    first_cell = column[0]
    first_cell_image = img[first_cell[1]:first_cell[1]+first_cell[3], first_cell[0]:first_cell[0]+first_cell[2]]
    first_cell_text = PT.image_to_string(first_cell_image).strip()
    #print(first_cell_text)
    if not is_similar(first_cell_text, 'NPS', threshold=80):  # 80 is just an example threshold
        raise ValueError(f'First cell does not contain the expected title, got {first_cell_text} instead')

    for i, coords in enumerate(column):
        if i == 0:  # Skip the title cell after the check
            continue
        
        # Preprocess the image (if necessary)
        processed_cell = preprocess_image(img, coords)

        '''
        #Show each cell being fed to have a visualization and be able to improve the preprocessing

        cv2.imshow('Processed cell',processed_cell)
        cv2.waitKey(0)
        '''

        #Configuration based on column
        custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789/X\"'
        # Extract text from the cell using OCR
        text = PT.image_to_string(processed_cell, config=custom_config).strip()
        # Append the text to the data list
        data.append(text)

    # Since the first cell was skipped, the index should be offset by 1
    df = pd.DataFrame(data, columns=['NPS'])
    #print(df)

    return df

