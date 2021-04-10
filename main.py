from PIL import Image
import sys
import numpy as np
from functions import check_black_pixel

filename = sys.argv[1]
MAX_BLACK_COLOR = 132

try:
    image = Image.open(filename)
except FileNotFoundError:
    print("File " + filename + " not found.")

# convert image into array
data = np.asarray(image)

# True if considered black, False otherwise
black_color = data.mean(axis=2) <= MAX_BLACK_COLOR

# True if black pixel was checked by
checked = np.zeros(shape=black_color.shape, dtype=bool)


