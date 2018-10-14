import params
import os.path
import threading
import time
import sys
import pandas as pd
import traceback
from os import remove
import numpy as np
from datetime import datetime
import requests
from our_lc_analyzer import OurLCAnalyzer

class MaxiLightCurves:
    

    __db = params.db
    __client = params.client
    __sources = None
    __errors  = []

    def manage_sources(self, p_source,p_type='daily'):
        print("Tratando "+p_source['source'])
        file_path = os.path.abspath('.')
        name = p_source['source'].replace(" ","_")
        url = None
        filename = None
        if p_type == 'orbital':
            name = name+'.orbital.txt'
            filename = os.path.join(file_path,'maxi_LCs',name)
            url = p_source['ligth_curves']['orbital']
        else:
            name = name+'.daily.txt'
            filename = os.path.join(file_path,'maxi_LCs',name)
            url = p_source['ligth_curves']['daily']

        try:
            page = requests.get(url)
            make_update = True
            if page.status_code == 200:
                texto = page.text
                p_source['lc'] = texto
                p_source['last_update'] = datetime.now() 
                #Descomentar si es necesario
                #p_source.pop('bokeh',None)
            else:
                make_update = False
                self.__errors.append(name)

            if make_update:
                print("Grabando "+p_source['source'])
                self.__db['sources'].save(p_source)
                print(p_source['source']+' Grabado')
                myClasif = OurLCAnalyzer()
                myClasif.getClasif(p_source['mission'],p_source['source'])
            
        except:
            print(traceback.format_exc())
            self.__errors.append(name)

    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'mission':id},no_cursor_timeout=True)

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources,p_type='daily'):
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

if __name__ == '__main__':
    mission = 'maxi'
    myLc = MaxiLightCurves(mission)
    maxiSources = myLc.getAllSources()

    if len(sys.argv)>1 and sys.argv[1] in ['-o','--orbital']:
        myLc.downloadLC(maxiSources,'orbital')
    else:
        myLc.downloadLC(maxiSources)
