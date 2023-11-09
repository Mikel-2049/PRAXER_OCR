from collections import defaultdict

def detect_columns(cells):
    # Create a dictionary to hold cells by their starting x-coordinate
    columns = defaultdict(list)
    
    # Group cells by their starting x-coordinate
    for cell in cells:
        columns[cell[0]].append(cell)
    
    # Sort cells within each column by their y-coordinate to maintain vertical order
    for col in columns.values():
        col.sort(key=lambda x: x[1])
    
    # Return the columns sorted by the x-coordinate of the first cell in each column
    return [columns[key] for key in sorted(columns)]



