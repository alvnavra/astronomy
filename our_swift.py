from urllib.request import urlretrieve
from astropy.io import fits
from astropy.table import Table
import os
import params

class Swift:
    
    __url = params.url
    __db = params.db
    __client = params.client
    
    def __init__(self,id):
        fits = self.__db['parameters']
        rdo = fits.find_one(id)
        self.__url = rdo['urls'][0]['catalog_fits']

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
        names = data.names
        names[0] = 'SOURCE'
        srcs = self.__db['sources']
        url_base_lc = 'https://swift.gsfc.nasa.gov/results/transients/weak/'

        rows = range(0,len(data))        
        for r in rows:
            row = data[r]
            cols = range(0,len(data.names))
            dict_row = {'tool_name':tool_name}
            for c in cols:
                if isinstance(row[c],(str)):
                    dict_row[names[c].lower()] = (row[c].replace('\x00','').replace('NULL','')).replace('?','')
                else:
                    dict_row[names[c].lower()] = row[c].item()
            print (dict_row)
            url_lc = url_base_lc+dict_row['source'].replace(' ','').replace('+','p')
            dict_lc_urls = {'daily':url_lc+'.lc.txt','orbital':url_lc+'.orbit.lc.txt'}
            dict_row['ligth_curves'] = dict_lc_urls
            srcs.update({'source':dict_row['source']},dict_row,upsert=True)


    def readSources(self, tool_name):
        params = self.__db['parameters'].find_one({'_id':tool_name})
        url_swift = params['urls'][0]['sources']
        '''TODO: La parte de encontrar las urls funciona. Comprobar la parte de tratarlas, que es
           la que viene a continuación'''
        exit(0)
        srcs = self.__db['sources'].find_one({'tool_name':tool_name},{'sources':1,'_id':0})['sources']
        for src in srcs:
            modified_src = src.replace(' ','').replace('+','p')
            url_fit = url_swift+modified_src+'.lc.fits'
            self.downloadFits(url_fit, modified_src,os.path.abspath('.')+'/fits')
            #self.readFitsData(modified_src,os.path.abspath('.')+'/fits')


        
if __name__ == '__main__':
    tool_name = 'swift'
    myFits = Swift(tool_name)
    url = myFits.getUrl()
    l_name = url.split('/')
    name = l_name[-1]
    myFits.downloadFits(url,name)
    myFits.readFits(tool_name, name)
    #myFits.readSources(tool_name)

