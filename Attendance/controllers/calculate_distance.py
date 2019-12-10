def calculate_location_distance(x1, y1, x2, y2):
    if (float(x1) - float(x2)) ** 2 + (float(y1) - float(y2)) ** 2 < 1:
        return True
    return False
