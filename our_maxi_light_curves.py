import params
import os.path
from urllib.request import urlretrieve
import threading
import time

class MaxiLightCurves:
    

    __db = params.db
    __client = params.client
    __sources = None
    __errors  = []

    def manage_sources(self, p_source):
        file_path = os.path.abspath('.')
        name_orbital = (p_source['source']+'.orbital.lc.txt').replace('+','p').replace(' ','')
        name_day = (p_source['source']+'.day.lc.txt').replace('+','p').replace(' ','')
        filename_orbital = os.path.join(file_path,'maxi_LCs',name_orbital)
        #filename_day = os.path.join(file_path,'maxi_LCs',name_day)
        url_orbital = p_source['ligth_curves']['orbital']
        #url_day = p_source['ligth_curves']['daily']
        name = ''
        try:
            name = filename_orbital
            print(name)
            urlretrieve(url_orbital,filename=name)
            #name = filename_day
            #urlretrieve(url_day,filename=name)
        except:
            self.__errors.append(name)

    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id})

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources):
        threads = []
        t = None

        for source in p_sources:
            t = threading.Thread(target=self.manage_sources, args=(source,),daemon=True, name=source['source'])
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
    tool_name = 'maxi'
    myLc = MaxiLightCurves(tool_name)
    maxiSources = myLc.getAllSources()
    myLc.downloadLC(maxiSources)
    pass
