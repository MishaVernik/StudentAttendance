def calcLocationDiff(x1, y1, x2, y2):
    if (float(x1) - float(x2)) ** 2 + (float(y1)-float(y2))**2 < 10:
        return True
    return False