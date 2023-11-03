import pytesseract as PT
from detect_cells import find_cells
from detect_columns import detect_columns
from process_item import read_item


def main():
    image = 'Images\Tabla_50024D_prueba_1.png'
    cell_regions, num_rows, num_columns = find_cells(image)
    columns = detect_columns(cell_regions)
    item_column = read_item(image, columns[0])

if __name__ == "__main__":
    main()