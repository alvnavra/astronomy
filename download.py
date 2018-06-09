from urllib.request import urlretrieve
from astropy.io import fits
from our_swift import Swift
from our_maxi import Maxi
from our_fermi import Fermi

'''urlretrieve('https://swift.gsfc.nasa.gov/results/transients/BAT_catalog.fits','BAT_catalog.fits')

from our_fits import Fits
from astropy.io import fits
from nasa_transient_weaks import nTransientWeaks
import urllib.request'''

fits = 3
if fits == 1:
    tool_name = 'swift'
    myFits = Swift(tool_name)
    url = myFits.getUrl()
    l_name = url.split('/')
    name = l_name[-1]
    myFits.downloadFits(url,name)
    myFits.readFits(tool_name, name)
    #myFits.readSources(tool_name)
elif fits == 2:
    tool_name = 'maxi'
    my_maxi = Maxi(tool_name)
    url = my_maxi.getUrl()
    my_maxi.readSources(url,tool_name)
elif fits == 3:    
    tool_name = 'fermi'
    my_fermi = Fermi(tool_name)
    url = my_fermi.getUrl()
    my_fermi.readSources(url,tool_name)

exit(0)
tool_name = 'fermi'
my_fermi = Fermi(tool_name)
url = my_fermi.getUrl()
my_fermi.readSources(url,tool_name)

tool_name = 'maxi'
my_maxi = Maxi(tool_name)
url = my_maxi.getUrl()
my_maxi.readSources(url,tool_name)

tool_name = 'swift'
myFits = Swift(tool_name)
url = myFits.getUrl()
l_name = url.split('/')
name = l_name[-1]
myFits.downloadFits(url,name)
myFits.readFits(tool_name, name)
#myFits.readSources(tool_name)'''
