import params
import os.path
from urllib.request import urlretrieve
import threading
import time
import sys
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show, output_file
from io import StringIO
import traceback

class MaxiLightCurves:
    

    __db = params.db
    __client = params.client
    __sources = None
    __errors  = []

    def manage_sources(self, p_source,p_type='daily'):
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
            print(name)
            urlretrieve(url,filename=filename)
            print (filename)
            df = pd.read_csv(filename, sep='\s+', header=None)
            new1 = df[(df > 0).all(1)]
            p = figure(x_axis_label='Hardness ratio', y_axis_label='FLUX')
            p.circle(new1[5]/(new1[3]), new1[5]+new1[3], size=4)
            filename_html = p_source['source'].replace(' ','_')+'.html'
            print(filename_html)
            fich = output_file(fielname_html)            
            p.show()

            


        except:

            self.__errors.append(name)

    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id}).limit(3)

    def getAllSources(self):
        return self.__sources

    def downloadLC(self, p_sources,p_type='daily'):
        threads = []
        t = None

        for source in p_sources:
            t = threading.Thread(target=self.manage_sources, args=(source,p_type,),daemon=True, name=source['source'])
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

    if len(sys.argv)>1 and sys.argv[1] in ['-o','--orbital']:
        myLc.downloadLC(maxiSources,'orbital')
    else:
        myLc.downloadLC(maxiSources)
