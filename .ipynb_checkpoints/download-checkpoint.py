from urllib.request import urlretrieve
from astropy.io import fits
from our_fits import Fits
from our_maxi import Maxi
from our_fermi import Fermi

'''urlretrieve('https://swift.gsfc.nasa.gov/results/transients/BAT_catalog.fits','BAT_catalog.fits')

from our_fits import Fits
from astropy.io import fits
from nasa_transient_weaks import nTransientWeaks
import urllib.request'''

fits = 3
if fits == 1:
    mission = 'swift'
    myFits = Fits(mission)
    url = myFits.getUrl()
    l_name = url.split('/')
    name = l_name[-1]
    myFits.downloadFits(url,name)
    #myFits.readFits(mission, name)
    myFits.readSources(mission)
elif fits == 2:
    mission = 'maxi'
    my_maxi = Maxi(mission)
    url = my_maxi.getUrl()
    my_maxi.readSources(url,mission)
elif fits == 3:    
    mission = 'fermi'
    my_fermi = Fermi(mission)
    url = my_fermi.getUrl()
    my_fermi.readSources(url,mission)

