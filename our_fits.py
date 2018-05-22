from urllib.request import urlretrieve
from astropy.io import fits
import os
import params

class Fits:
    
    __url = params.url
    __db = params.db
    __client = params.client
    
    def __init__(self,id):
        fits = self.__db['parameters']
        rdo = fits.find_one(id)
        self.__url = rdo['url']

    def getUrl(self):
        return self.__url

    def downloadFits(self, url, name, path = None):
        if path == None:
            urlretrieve(url,name)
        else:
            urlretrieve(url,os.path.join(path,name))

    def readFitsData(self, name, path=None):
        file = ''
        if path != None:
            file = os.path.join(path,name)
        else:
            file = name
        hdul = fits.open(file)
        for idx in range(0,len(hdul)):
            if hdul[idx].data != None:
                hdr = hdul[idx].header
                src_name = hdr['SRC_NAME']
                keys = list(hdr.keys())
                i = 0
                
                for key in keys:
                    #print (hdul[idx].header[i])
                    print (hdul[idx].data[i])
                    cols = len(hdul[idx].data[i])
                    numHeader = 1
                    headers = ['TFORM','TTYPE','TUNIT']
                    num = 1
                    rng = range(0,cols)
                    for col in  rng:
                        if col%3 == 0:
                            num = num+1       
                            numHeader = numHeader+1
                        header = headers[col%3]+str(numHeader)
                        print (header)
                print(repr(hdr))
        
    def readFits(self, tool_name, name, path=None):
        file = ''
        if path != None:
            file = os.path.join(path,name)
        else:
            file = name

        hdul = fits.open(file)
        data = hdul[1].data
        lista = data.field(0)
        print (lista)
        print (len(lista))
        source_list = []
        srcs = self.__db['sources']
        dict_source = {}
        dict_source['tool_name'] = tool_name
        l_sources = []
        rng = range(0,len(lista))
        for r in rng:
            l_sources.append(lista[r])
        dict_source['sources'] = l_sources
        srcs.save(dict_source)


    def readSources(self, tool_name):
        params = self.__db['parameters'].find_one({'_id':tool_name})
        url_nasa = params['url_sources']
        srcs = self.__db['sources'].find_one({'tool_name':tool_name},{'sources':1,'_id':0})['sources']
        for src in srcs:
            modified_src = src.replace(' ','').replace('+','p')
            url_fit = url_nasa+modified_src+'.lc.fits'
            self.downloadFits(url_fit, modified_src,os.path.abspath('.')+'/fits')
            self.readFitsData(modified_src,os.path.abspath('.')+'/fits')


        
