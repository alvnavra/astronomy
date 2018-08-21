import params
import pandas as pd
import numpy as np
import BayesianBlocks
from matplotlib import pyplot as plt
from io import StringIO


class OurBayesianBlocks:

    __url = params.url
    __db = params.db
    __client = params.client
    __blks = None
    __lc = None

    def __init__(self,tool_name,source):
        lc = self.__sources = self.__db['sources'].find({'tool_name':tool_name,'source':source},{'lc':1,'_id':0})
        LC_Data = StringIO(lc[0]['lc'])
        df = pd.read_csv(LC_Data, sep='\s+', header=None)
        
        self.__lc = df

        dict_data = {}
        dict_data['t'] = df[0]
        dict_data['x'] = df[1]
        dict_data['err'] = df[2]

        myBys = BayesianBlocks.BayesBlocks(dict_data)
        blk = myBys.blocks
        self.__blks = blk
        chp = blk['change_points']
        lchp = chp.tolist()
        x_blks = blk['x_blocks'].tolist()

        t_blocks = list(sum(blk['bins'], ()))  # Flatten list of tuples for plt.plot()
        x_temp = zip(blk['x_blocks'], blk['x_blocks'])
        x_blocks = list(sum(x_temp, ()))  # Flatten list of tuples for plt.plot()
        plt.plot(t_blocks, x_blocks)        
        #plt.show()

    def getOutbursts(self):

        median = self.__lc.median()[1]
        sigma = self.__lc.mad()[1]
        FWHM = 2 * np.sqrt(2*np.log(2))*sigma
        umbral = float(median + (sigma*FWHM))

        print("median --> %f" %median)
        print("sigma --> %f" %sigma)
        print("FWHTM --> %f" %FWHM)


        blks = self.__blks
        outburst = []

        x_blks = blks['x_blocks'].tolist()
        append_outburst = None
        for xb in x_blks:
            try:
                x_ini_blk1 = 0
                x_fin_blkn = 0
                if xb > umbral:
                    idx = x_blks.index(xb)
                    xb1 = x_blks[idx+1]
                    xb2 = x_blks[idx+2]
                    if xb1 > xb and xb2 > umbral and (append_outburst == True or append_outburst == None):                        
                        if (blks['bins'][idx][1]-blks['bins'][idx][0]>2 and blks['bins'][idx+1][1]-blks['bins'][idx+1][0]>2 and blks['bins'][idx+2][1]-blks['bins'][idx+2][0] > 2) :
                            x_ini_blk1 = blks['bins'][idx][0]
                            print("idx: %d" %idx)
                            print ("Outbust Found")
                            print(blks['bins'][idx][0])
                            outburst.append(1)
                            append_outburst = False
                if xb < umbral:
                    idx = x_blks.index(xb)
                    x_fin_blkn = blks['bin']['idx'][1]
                    activity_weigth = x_fin_blkn - x_ini_blk1
                    if activity_weigth < 7:
                        outburst.pop(-1)
                    append_outburst = True
            except:
                pass


        print("Number of Outbursts: "+str(len(outburst)))
        print("Threshold: "+str(umbral))

        

        rng = range(0,len(self.__lc[0]))
        lst = []
        for r in rng:
            lst.append(umbral)

        df_umbral = pd.DataFrame(data=lst)

        t_blocks = list(sum(blks['bins'], ()))  # Flatten list of tuples for plt.plot()
        x_temp = zip(blks['x_blocks'], blks['x_blocks'])
        x_blocks = list(sum(x_temp, ()))  # Flatten list of tuples for plt.plot()
        plt.plot(t_blocks, x_blocks) 
        plt.plot(self.__lc[0],df_umbral)
        plt.show()




if __name__ == '__main__':
    myBlk = OurBayesianBlocks('maxi','GS 0834-430 with GS 0836-429')
    myBlk.getOutbursts()