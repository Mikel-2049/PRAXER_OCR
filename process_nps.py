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
        #Configuration based on column
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789M/X\"'
        # Extract text from the cell using OCR
        text = PT.image_to_string(processed_cell, config=custom_config).strip()
        # Append the text to the data list
        data.append(text)

    # Since the first cell was skipped, the index should be offset by 1
    df = pd.DataFrame(data, columns=['NPS'])
    print(df)

    return df

