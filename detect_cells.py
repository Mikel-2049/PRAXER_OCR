import cv2
import matplotlib.pyplot as plt
import numpy as np


def load_image(image):
    """
    Load an image using OpenCV.
    """
    img_cv = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    return img_cv


def preprocess_image(image):
    """
    Preprocess the image for OCR.
    """
    _, thresh_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    return thresh_img


def detect_lines(image, horizontal_size=40, vertical_size=20):
    """
    Detects horizontal and vertical lines in the given image.
    
    Parameters:
        image (ndarray): The input image in which lines need to be detected.
        horizontal_size (int, optional): Size of the horizontal structure element. Default is 40.
        vertical_size (int, optional): Size of the vertical structure element. Default is 20.
    
    Returns:
        horizontal_lines_img (ndarray): Image containing detected horizontal lines.
        vertical_lines_img (ndarray): Image containing detected vertical lines.
    """
    # Define structure elements for horizontal and vertical lines
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    
    # Detect horizontal lines
    horizontal_lines_img = cv2.erode(image, horizontal_structure, iterations=1)
    horizontal_lines_img = cv2.dilate(horizontal_lines_img, horizontal_structure, iterations=1)
    
    # Detect vertical lines
    vertical_lines_img = cv2.erode(image, vertical_structure, iterations=1)
    vertical_lines_img = cv2.dilate(vertical_lines_img, vertical_structure, iterations=1)
    
    return horizontal_lines_img, vertical_lines_img


def standardize_line_thickness(image, standard_thickness=2):
    """
    Standardize the thickness of lines in the given image.
    
    Parameters:
        image (ndarray): The input image containing lines.
        standard_thickness (int, optional): The standard thickness to apply to all lines. Default is 2.
    
    Returns:
        standardized_lines (ndarray): Image containing lines with standardized thickness.
    """
    # Find contours in the image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize an empty image to draw standardized lines
    standardized_lines = np.zeros_like(image)
    
    # Draw each contour with standard thickness
    for contour in contours:
        cv2.drawContours(standardized_lines, [contour], -1, 255, thickness=standard_thickness)
    
    return standardized_lines

def create_cell_mask(horizontal_lines, vertical_lines):
    """
    Combines horizontal and vertical lines to create a mask for cell identification.
    
    Parameters:
        horizontal_lines (ndarray): Image containing horizontal lines.
        vertical_lines (ndarray): Image containing vertical lines.
    
    Returns:
        cell_mask (ndarray): Image containing combined lines serving as a mask for cell identification.
    """
    # Combine horizontal and vertical lines
    cell_mask = cv2.addWeighted(horizontal_lines, 1, vertical_lines, 1, 0)
    
    return cell_mask

def identify_individual_black_cells(mask):
    """
    Identifies individual black cell regions in the rows based on the given mask.
    
    Parameters:
        mask (ndarray): Image containing the mask for cell identification.
    
    Returns:
        cell_regions (list): List of tuples containing coordinates (x, y, w, h) for each cell in the rows.
        num_rows (int): Number of rows detected.
    """
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (mask.shape[1]//40, 1))
    horizontal_lines = cv2.morphologyEx(mask, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    cnts, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of horizontal lines, which will give us the number of rows
    num_rows = len(cnts)

    # Invert the mask so that black cells become white (which is easier for contour detection)
    inverted_mask = cv2.bitwise_not(mask)
    
    # Find contours in the inverted mask
    contours, _ = cv2.findContours(inverted_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize list to store cell regions
    cell_regions = []
    
    # Sort contours by their y-coordinate to process rows in order
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    
    # Identify cell regions for the rows
    row_count = 0
    prev_y = -1
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Check if we've moved to a new row
        if y != prev_y:
            row_count += 1
            if row_count > num_rows:
                break
        
        # Check if the region is a valid cell (not just a line)
        if w < mask.shape[1] and h > 1:
            # Add the cell region to the list
            cell_regions.append((x, y, w, h))
        
        # Update previous y-coordinate
        prev_y = y
    
    return cell_regions, num_rows


def calculate_cell_thresholds(cell_regions):
    total_height = 0
    total_width = 0
    num_cells = len(cell_regions)

    for x, y, w, h in cell_regions:
        total_height += h
        total_width += w
    
    avg_height = total_height / num_cells
    avg_width = total_width / num_cells
    
    height_threshold = avg_height * 0.6
    width_threshold = avg_width * 0.3
    
    return height_threshold, width_threshold


def prune_cell_regions(cell_regions, height_threshold, width_threshold):
    pruned_regions = [region for region in cell_regions if region[3] >= height_threshold and region[2] >= width_threshold]
    return pruned_regions


def calculate_grid_dimensions(cell_regions):
    # Your logic to determine the number of rows and columns
    # For example, you might look for distinct Y-coordinates for rows
    # and distinct X-coordinates for columns among your cell regions
    
    row_coordinates = [region[1] for region in cell_regions]  # Assuming region = (x, y, w, h)
    unique_row_coordinates = list(set(row_coordinates))
    num_rows = len(unique_row_coordinates)
    
    col_coordinates = [region[0] for region in cell_regions]  # Assuming region = (x, y, w, h)
    unique_col_coordinates = list(set(col_coordinates))
    num_columns = len(unique_col_coordinates)
    
    return num_rows, num_columns





def find_cells(image):
    img = load_image(image)

    # Preprocess the loaded image
    preprocessed_img = preprocess_image(img)

    # Detect lines
    horizontal_lines_img, vertical_lines_img = detect_lines(preprocessed_img)

    #Standarized lines
    standarized_lines = standardize_line_thickness(horizontal_lines_img)

    #Create a cell mask
    cell_mask = create_cell_mask(standarized_lines, vertical_lines_img)

    cell_regions, num_rows = identify_individual_black_cells(cell_mask)

    #print(num_rows)

    # Calculate height and width thresholds
    height_threshold, width_threshold = calculate_cell_thresholds(cell_regions)

    # Prune the cell regions based on the calculated thresholds
    pruned_cell_regions = prune_cell_regions(cell_regions, height_threshold, width_threshold)

    '''
    # Create a copy of the original image for visualization 
    image_copy = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) ## Can be deleted 

    # Draw rectangles around each detected cell
    for x, y, w, h in pruned_cell_regions: # Can be deleted
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Plot the image
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
    plt.title('Cell Regions')
    plt.axis('off')
    plt.show()
    '''

    num_rows, num_columns = calculate_grid_dimensions(pruned_cell_regions)

    '''
    print(num_columns)
    print(num_rows)
    '''

    return pruned_cell_regions, num_rows, num_columns
