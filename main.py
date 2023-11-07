import pytesseract as PT
from detect_cells import find_cells
from detect_columns import detect_columns
from process_item import read_item
from process_item_code import read_item_code
from process_tag import read_tag
from process_quantity import read_quantity
from process_nps import read_nps


def main():
    image = 'Images\Img_19_r_t3.png'
    cell_regions, num_rows, num_columns = find_cells(image)
    columns = detect_columns(cell_regions)
    item_column = read_item(image, columns[0])
    item_code_column = read_item_code(image, columns[1], num_rows)
    tag_column = read_tag(image, columns[2], num_rows)
    quantity_column = read_quantity(image, columns[3], num_rows)
    nps_column = read_nps(image, columns[4], num_rows)

if __name__ == "__main__":
    main()