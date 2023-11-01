import cv2

def grayscale_image(image):
    gray_image = cv2.GRAYSCALE(image)
    return gray_image

def preprocess_image(gray_image):
    _, tresh_img = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)
    return tresh_img

def detect_lines(thresh_img, horizontal_size, vertical_size):
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))


def find_cells(image):

    return contours, num_rows
