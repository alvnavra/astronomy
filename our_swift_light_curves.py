import params
import os.path
from urllib.request import urlretrieve
import threading
import time
import sys

class SwiftLigthCurves:
    
    __url = 'https://swift.gsfc.nasa.gov/results/transients/'
    __url_weak = 'https://swift.gsfc.nasa.gov/results/transients/weak/'

    __db = params.db
    __client = params.client
    __sources = None
    __errors  = []

    def manage_sources(self, p_source,p_type='daily'):
        file_path = os.path.abspath('.')
        name = None        
        if p_type == 'orbital':
            name = (p_source['source']+'.orbit.lc.txt').replace(' ','_')
            url_source = (self.__url_weak+p_source['source']+'.orbit.lc.txt').replace('+','p').replace(' ','')
            url_source2 = (self.__url+p_source['source']+'.orbit.lc.txt').replace('+','p').replace(' ','')
        else:
            name = (p_source['source']+'lc.txt').replace(' ','_')
            url_source = (self.__url_weak+p_source['source']+'.lc.txt').replace('+','p').replace(' ','')
            url_source2 = (self.__url+p_source['source']+'.lc.txt').replace('+','p').replace(' ','')
        
        filename = os.path.join(file_path,'swift_LCs',name)
        print (filename)
        try:
            urlretrieve(url_source,filename=filename)
        except:
            try:
                urlretrieve(url_source2,filename=filename)
            except:
                print("error -->"+name)
                print("error -->"+url_source)
                print("error -->"+url_source2)
                self.__errors.append(name)

    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id},no_cursor_timeout=True)

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources, p_type='daily'):
        threads = []
        t = None

        for source in p_sources:
            t = threading.Thread(target=self.manage_sources, args=(source,p_type), daemon=True, name=source['source'])
            threads.append(t)
            t.start()
            if len(threads) % 6 == 0:
                t.join()
                threads = []

        t.join()

        print ("===========================")
        print ("Erroneos")
        print ("===========================")
        for error in self.__errors:
            print (error)

        

if __name__ == '__main__':
    tool_name = 'swift'
    myLc = SwiftLigthCurves(tool_name)
    swiftSources = myLc.getAllSources()
    if sys.argv[1] in ['-o','--orbital']:
        myLc.downloadLC(swiftSources,'orbital')
    else:
        myLc.downloadLC(swiftSources)
