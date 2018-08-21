import params
import os.path
from urllib.request import urlretrieve
import threading
import time
import sys
import pandas as pd
from bokeh.plotting import figure, save
from bokeh.io import output_file
import traceback
from os import remove
import numpy as np
import BayesianBlocks
from datetime import datetime
from matplotlib import pyplot as plt

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
            buffer = open(filename, 'rt').read()
            p_source['lc'] = buffer
            df = pd.read_csv(filename, sep='\s+', header=None)            
            new1 = df[(df > 0).all(1)]

            '''dict_data = {}
            dict_data['t'] = df[0]
            dict_data['x'] = df[1]
            dict_data['err'] = df[2]

            myBys = BayesianBlocks.BayesBlocks(dict_data)
            blk = myBys.blocks
            chp = blk['change_points']
            lchp = chp.tolist()
            change_points = p_source['change_points']
            x_blks = blk['x_blocks'].tolist()

            latest_change_point = {}
            ptg_variation = 0
            if change_points == None:
                change_points = []
            else:
                latest_change_point =  {'date':datetime.now(),'change_points':len(lchp)}
                previous_change_point = change_points[len(change_points)-1]
                if previous_change_point != latest_change_point['change_points']:
                    ptg_variation = latest_change_point['change_points']'''



            '''p_source['change_points'].change_points
            if len(p_source['change_points']) > 1:'''


            p = figure(x_axis_label='Hardness ratio', y_axis_label='FLUX')
            p.circle(new1[5]/(new1[3]), new1[5]+new1[3], size=4)
            filename_html = filename.replace('txt','html')
            output_file(filename_html)
            save(p)
            p_source['bokeh'] = open(filename_html,'rt').read()
            self.__db['sources'].save(p_source)
        except:
            print(traceback.format_exc())
            self.__errors.append(name)

    def __init__(self,id):
        self.__sources = self.__db['sources'].find({'tool_name':id,'source':'GS 0834-430 with GS 0836-429'})

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
