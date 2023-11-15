import pytesseract as PT
import os
import pandas as pd
from detect_cells import find_cells
from detect_columns import detect_columns
from process_item import read_item
from process_item_code import read_item_code
from process_tag import read_tag
from process_quantity import read_quantity
from process_nps import read_nps
from process_material_description import read_material_description
from merge_columns import merge_columns


def process_image(image_path):
    cell_regions, num_rows, num_columns = find_cells(image_path)
    columns = detect_columns(cell_regions)
    item_column = read_item(image_path, columns[0])
    item_code_column = read_item_code(image_path, columns[1], num_rows)
    tag_column = read_tag(image_path, columns[2], num_rows)
    quantity_column = read_quantity(image_path, columns[3], num_rows)
    nps_column = read_nps(image_path, columns[4], num_rows)
    material_description_column = read_material_description(image_path, columns[5], num_rows)

    return merge_columns(
        item_column,
        item_code_column,
        tag_column,
        quantity_column,
        nps_column,
        material_description_column
    )

def main():
    folder_path = 'Images'
    all_dataframes = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):  # Assuming all images are in .png format
            image_path = os.path.join(folder_path, filename)
            df = process_image(image_path)
            all_dataframes.append(df)

    final_dataframe = pd.concat(all_dataframes, ignore_index=True)
    print(final_dataframe)


if __name__ == "__main__":
    main()