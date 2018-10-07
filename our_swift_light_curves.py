import params
import threading
import time
import sys
import requests
from datetime import datetime
import re
from our_bayesian_blocks import OurBayesianBlocks

class SwiftLigthCurves:
    
    __url = 'https://swift.gsfc.nasa.gov/results/transients/'
    __url_weak = 'https://swift.gsfc.nasa.gov/results/transients/weak/'

    __db = params.db
    __client = params.client
    __sources = None
    __errors  = []

    def __return_lc(self, p_text):
        return re.sub('^ ','',(re.sub('#','\n',(re.sub('\s+',' ',re.sub('\n','#',re.sub('#.*\n','\n', p_text)))).replace('#####',''))).replace('\n ','\n'))

    def manage_sources(self, p_source,p_type='daily'):
        print("Tratando "+p_source['source'])
        url_source = p_source['url_lc_daily']
        url_source2 = (self.__url+p_source['source']+'.lc.txt').replace('+','p').replace(' ','')
        
        page = requests.get(url_source)
        make_update = True
        if page.status_code == 200:
            texto = self.__return_lc(page.text)
            p_source['lc'] = texto
            p_source['last_update'] = datetime.now()            
        else:
            page = requests.get(url_source2)
            if page.status_code == 200:
                texto = self.__return_lc(page.text)
                p_source['lc'] = texto
                p_source['last_update'] = datetime.now()
            else:
                make_update = False
                self.__errors.append(p_source['source'])

        if make_update:
            print("Grabando "+p_source['source'])
            self.__db['sources'].replace_one({'tool_name':p_source['tool_name'],
                                         'source':p_source['source']
                                        }, p_source)
            print(p_source['source']+' Grabado')
            print("========================================")
            print("Calculando Bayesian Blocks")
            print("========================================")
            bayBlock = OurBayesianBlocks()
            bayBlock.calculate_bayesian_blocks('swift',p_source['source'])
            print("Buscando Outbursts de :"+p_source['source'])
            outbursts =  bayBlock.getOutbursts(p_source['source'])
            if len(outbursts) > 0:
                p_source['outbursts'] = outbursts
                p_source['last_update'] = datetime.now()
                self.__db['sources'].replace_one({'tool_name':p_source['tool_name'],
                                            'source':p_source['source']
                                            }, p_source)


    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id},no_cursor_timeout=True)

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources, p_type='daily'):
        inicio = datetime.now()
        threads = []
        t = None        
        for source in p_sources:
            t = threading.Thread(target=self.manage_sources, args=(source,p_type), daemon=True, name=source['source'])
            threads.append(t)
            if len(threads) % 20 == 0:
                for t1 in threads:
                    t1.start()
                for t1 in threads:
                    t1.join()
                threads = []

        for t1 in threads:
            t1.start()
        for t1 in threads:
            t1.join()


        print ("===========================")
        print ("Erroneos")
        print ("===========================")
        for error in self.__errors:
            print (error)

        final = datetime.now()
        elapsed = final-inicio
        print('Time elapsed (hh:mm:ss.ms) {}'.format(elapsed))

        

if __name__ == '__main__':
    tool_name = 'swift'
    myLc = SwiftLigthCurves(tool_name)
    swiftSources = myLc.getAllSources()
    myLc.downloadLC(swiftSources)
