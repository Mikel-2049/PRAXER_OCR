from utils import is_similar

import pandas as pd
import cv2
from pytesseract import pytesseract as PT


PT.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def read_item(image_path, column):
    img = cv2.imread(image_path)
    data = []
    for i, (x, y, w, h) in enumerate(column):
        cell = img[y:y+h, x:x+w]
        text = PT.image_to_string(cell).strip()
        #print(f"Cell {i}: '{text}'")

        if i == 0:
            # Use similarity check for the first cell
            if not is_similar(text, 'ITEM'):
                raise ValueError('First cell should contain "ITEM"', text)
        else:
            if not text or text.isspace():
                # Append index if cell is empty
                data.append(i)
            else:
                try:
                    number = int(text)
                    data.append(number)
                except ValueError:
                    # Instead of raising an error, append the index if the cell text is not a number
                    data.append(i)
    
    # Create DataFrame with the 'ITEM' column
    df = pd.DataFrame(data, columns=['ITEM'])
    print(df)
    return df






