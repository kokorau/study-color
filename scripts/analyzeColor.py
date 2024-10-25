import coloria
import json
import numpy as np

with open('../data/raw/rgbPalette.json', 'r') as file:
    data = json.load(file)

data = np.array(data)

# flatten the data
data = data.reshape(-1, 3)
