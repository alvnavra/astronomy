import params
import os.path
from urllib.request import urlretrieve

class SwiftLigthCurves:
    
    __url = 'https://swift.gsfc.nasa.gov/results/transients/'
    __url_weak = 'https://swift.gsfc.nasa.gov/results/transients/weak/'

    __db = params.db
    __client = params.client
    __sources = None
    
    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id})

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources):
        for source in p_sources:
            file_path = os.path.abspath('.')
            name = source['source']+'.txt'
            filename = os.path.join(file_path,'swift_LCs',name)
            url_source = (self.__url_weak+source['source']+'.lc.txt').replace('+','p').replace(' ','')
            url_source2 = (self.__url+source['source']+'.lc.txt').replace('+','p').replace(' ','')
            print (url_source)
            try:
                urlretrieve(url_source,filename=filename)
            except:
                urlretrieve(url_source2,filename=filename)

            


if __name__ == '__main__':
    tool_name = 'swift'
    myLc = SwiftLigthCurves(tool_name)
    swiftSources = myLc.getAllSources()
    myLc.downloadLC(swiftSources)
    pass
