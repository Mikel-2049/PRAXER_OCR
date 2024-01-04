import cv2
from pytesseract import pytesseract as PT
from fuzzywuzzy import fuzz

from process_item import read_item
from process_item_code import read_item_code
from process_tag import read_tag
from process_quantity import read_quantity
from process_nps import read_nps
from process_material_description import read_material_description

def is_header_similar(ocr_header, expected_header, threshold=67):
    """
    Check if the OCR header is similar enough to the expected header.
    A threshold can be set to tune the sensitivity.
    """
    return fuzz.ratio(ocr_header.upper(), expected_header.upper()) >= threshold

def read_headers(image_path, columns):
    img = cv2.imread(image_path)
    headers = []
    for column in columns:
        x, y, w, h = column[0]  # Assuming the first cell is the header
        cell = img[y:y+h, x:x+w]
        text = PT.image_to_string(cell).strip()
        headers.append(text)
    return headers

def get_column_function_map(num_rows):
    return {
        'ITEM': (read_item, []),
        'ITEM CODE': (read_item_code, [num_rows]),
        'TAG': (read_tag, [num_rows]),
        'QUANTITY': (read_quantity, [num_rows]),
        'NPS': (read_nps, [num_rows]),
        'MATERIAL DESCRIPTION': (read_material_description, [num_rows]),
        # ... any other functions and their arguments
    }
