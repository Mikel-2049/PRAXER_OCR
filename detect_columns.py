def detect_columns(cells):
    # Find the unique x-coordinates of the cell boundaries
    x_boundaries = sorted({cell[0] for cell in cells})
    
    # Initialize the list of columns
    columns = [[] for _ in range(len(x_boundaries) - 1)]
    
    # Assign each cell to a column based on its x-coordinate
    for cell in cells:
        for i in range(len(x_boundaries) - 1):
            left = x_boundaries[i]
            right = x_boundaries[i + 1]
            if left <= cell[0] < right:
                columns[i].append(cell)
                break
    
    return columns



