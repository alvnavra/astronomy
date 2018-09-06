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
        dict_data['x'] = df[5] # Banda entre 4 y 10 keV
        dict_data['err'] = df[6] # Error producido en la banda anterior.

        myBys = BayesianBlocks.BayesBlocks(dict_data)
        blk = myBys.blocks
        self.__blks = blk
        chp = blk['change_points']
        lchp = chp.tolist()
        x_blks = blk['x_blocks'].tolist()

        t_blocks = list(sum(blk['bins'], ()))  # Flatten list of tuples for plt.plot()
        x_temp = zip(blk['x_blocks'], blk['x_blocks'])
        x_blocks = list(sum(x_temp, ()))  # Flatten list of tuples for plt.plot()
        #plt.plot(t_blocks, x_blocks)        
        #plt.show()

    def getOutbursts(self):

        median = self.__lc.median()[1]
        sigma = self.__lc.mad()[1]
        FWHM = 2 * np.sqrt(2*np.log(2))*sigma
        umbral = (float(median + (sigma*FWHM)))/2

        print("median --> %f" %median)
        print("sigma --> %f" %sigma)
        print("FWHTM --> %f" %FWHM)


        blks = self.__blks
        outburst = []

        x_blks = blks['x_blocks'].tolist()
        activity_blocks = []

        append_outburst = None
        idx = 0
        acceptance_pctge = 25
        min_width = 7

        for xb in x_blks:
            idx = x_blks.index(xb)
            if xb >= umbral and (append_outburst == True or append_outburst == None):                
                x_blk_ant = x_blks[idx-1]
                pctge = (x_blk_ant/xb)*100
                activity_blocks.append(blks['bins'][idx])
                width = activity_blocks[len(activity_blocks)-1][1]-activity_blocks[len(activity_blocks)-1][0]
                #if activity_blocks[len(activity_blocks)-1][0] >= 55000:
                #    print("Estoy aqui")
                append_outburst = True
                if pctge >= acceptance_pctge:                    
                    if width  >= min_width:
                        outburst.append(1)
                        print(pctge)
                        print ("Outbust Found")
                        print (activity_blocks[0][0])
                        append_outburst = False
                    else:
                        activity_blocks = []
                else:
                    activity_blocks = []
            if xb < umbral and append_outburst == False:
                if x_blks[idx+1] < umbral and x_blks[idx+2] < umbral:
                    append_outburst = True                    
                    activity_blocks = []


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
    #myBlk = OurBayesianBlocks('maxi','Aql X-1')
    #myBlk = OurBayesianBlocks('maxi','GS 0834-430 with GS 0836-429')
    myBlk = OurBayesianBlocks('maxi','4U 1630-472')
    #myBlk = OurBayesianBlocks('maxi','RX J0520.5-6932')
    #myBlk = OurBayesianBlocks('maxi','SAX J1747.0-2853')
    myBlk.getOutbursts()