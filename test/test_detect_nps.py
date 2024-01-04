import cv2
import pytesseract as pt
from fuzzywuzzy import fuzz

# Define a function to calculate the similarity between OCR output and expected text
def ocr_similarity(ocr_output, expected_output):
    return fuzz.token_sort_ratio(ocr_output, expected_output)

# Define a function to preprocess the image using various configurations
def preprocess_image(img, method, **kwargs):
    # Apply the preprocessing method based on the provided arguments
    if method == 'threshold':
        _, thresh = cv2.threshold(img, kwargs['thresh_val'], 255, cv2.THRESH_BINARY)
    elif method == 'adaptive_threshold':
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, kwargs['block_size'], kwargs['C'])
    elif method == 'canny':
        thresh = cv2.Canny(img, kwargs['threshold1'], kwargs['threshold2'])
    
    # Resize if scaling factor is provided
    if 'scale_factor' in kwargs:
        width = int(img.shape[1] * kwargs['scale_factor'])
        height = int(img.shape[0] * kwargs['scale_factor'])
        thresh = cv2.resize(thresh, (width, height), interpolation=cv2.INTER_AREA)
    
    return thresh

# Define a function to test different preprocessing configurations
def test_ocr_configs(image_path, coords, expected_output):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, y, w, h = coords
    roi = gray[y:y+h, x:x+w]

    # Define a set of different preprocessing configurations
    configs = [
        {'method': 'threshold', 'thresh_val': 100},
        {'method': 'threshold', 'thresh_val': 150},
        {'method': 'adaptive_threshold', 'block_size': 11, 'C': 2},
        {'method': 'adaptive_threshold', 'block_size': 15, 'C': 3},
        {'method': 'canny', 'threshold1': 50, 'threshold2': 150},
        # Add more configurations here
        # ...
    ]

    # Test each configuration
    best_score = 0
    best_config = None
    best_ocr_output = ""
    for config in configs:
        preprocessed_img = preprocess_image(roi, **config)
        ocr_output = pt.image_to_string(preprocessed_img, config='--psm 6').strip()
        score = ocr_similarity(ocr_output, expected_output)

        if score > best_score:
            best_score = score
            best_config = config
            best_ocr_output = ocr_output

    return best_config, best_ocr_output, best_score

# Usage:
# coords = (x, y, w, h)  # Replace with your actual coordinates
# expected_output = "Your expected OCR text here"
# best_config, best_ocr_output, best_score = test_ocr_configs('path/to/your/image.png', coords, expected_output)
# print("Best configuration:", best_config)
# print("Best OCR output:", best_ocr_output)
# print("Best similarity score:", best_score)