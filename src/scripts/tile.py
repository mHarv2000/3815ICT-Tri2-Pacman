import os
from glob import glob

g = os.path.join('..', 'img', 'pacman', '*.png')
gl = glob(g)

print(gl)
