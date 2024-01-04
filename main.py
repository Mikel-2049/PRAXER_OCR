import pytesseract as PT
import os
import pandas as pd
from detect_cells import find_cells
from detect_columns import detect_columns
from detect_headers import read_headers
from detect_headers import get_column_function_map
from detect_headers import is_header_similar
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
    headers = read_headers(image_path, columns)
    column_function_map = get_column_function_map(num_rows)

    data_columns = []
    for ocr_header, column in zip(headers, columns):
        matched = False
        for expected_header, (func, args) in column_function_map.items():
            if is_header_similar(ocr_header, expected_header):
                # Call the associated function with unpacked arguments
                data_columns.append(func(image_path, column, *args))
                matched = True
                break
        if not matched:
            print(f"Unexpected or unreadable header: {ocr_header}")
            data_columns.append(None)  # Placeholder for unexpected columns

    return merge_columns(*data_columns)

def main():
    folder_path = 'Images/NPS_Quantity'
    all_dataframes = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):  # Assuming all images are in .png format
            image_path = os.path.join(folder_path, filename)
            df = process_image(image_path)
            all_dataframes.append(df)

    final_dataframe = pd.concat(all_dataframes, ignore_index=True)
    print(final_dataframe)

    # Save to Excel file
    output_file = 'output.xlsx'  # Define the Excel file name
    final_dataframe.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()