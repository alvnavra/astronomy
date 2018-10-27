from astropy.io import fits
from astropy.table import Table
import pandas as pd
import os.path


file= os.path.join(os.path.abspath('.'),"gx1p4.fits")
hdu_list = fits.open(file)
datos = hdu_list[2]
a = Table.read(datos)
b = a.to_pandas()
print(b)