import pytesseract as PT
from detect_cells import find_cells

def main():
    image = 'Images\ReTabla_50024D_prueba_2.png'
    contours, num_rows = find_cells(image)

if __name__ == "__main__":
    main()