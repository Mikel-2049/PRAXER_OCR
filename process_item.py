import pandas as pd
import cv2
from pytesseract import pytesseract as PT

PT.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def read_item(image_path, column):
    img = cv2.imread(image_path)
    
    data = []
    for i, (x, y, w, h) in enumerate(column):
        # Extract region corresponding to current cell
        cell = img[y:y+h, x:x+w]
        
        # Extract text from cell using OCR
        text = PT.image_to_string(cell)
        text = text.strip()
        
        # Process text
        if i == 0:
            if text != 'ITEM':
                raise ValueError('First cell should contain "ITEM"')
        else:
            if not text or text.isspace():
                data.append(i)  # Append index if cell is empty
            else:
                try:
                    number = int(text)
                except ValueError:
                    raise ValueError(f'Cell {i} should contain a number or be empty')
                data.append(number)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['ITEM'])
    
    return df






