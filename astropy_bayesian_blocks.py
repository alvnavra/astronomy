import params
import pandas as pd
import numpy as np
from astropy.stats import bayesian_blocks as bays
from astropy.stats import histogram as histo
from matplotlib import pyplot as plt
from io import StringIO


class AstropyBayesianBlocks:

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

        #myBys = BayesianBlocks.BayesBlocks(dict_data)
        myBys = bays(dict_data['t'],dict_data['x'],dict_data['err'],fitness='measures',p0=0.05)
        plt.hist(df[0],bins=myBys)
        plt.show()
        hist, bin_edges = histo(myBys)
        hist = [0] + hist.tolist()
        bin_edges = bin_edges.tolist()
        plt.plot(bin_edges, hist)
        plt.show()
        exit(0)
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
        umbral = float(median + (sigma*FWHM))

        print("median --> %f" %median)
        print("sigma --> %f" %sigma)
        print("FWHTM --> %f" %FWHM)


        blks = self.__blks
        outburst = []

        x_blks = blks['x_blocks'].tolist()
        activity_blocks = []
        append_outburst = None
        idx = 0
        for xb in x_blks:
            x_ini_blk1 = 0
            x_fin_blkn = 0
            if xb >= umbral and (append_outburst == True or append_outburst == None):
                idx = x_blks.index(xb)
                activity_blocks.append(blks['bins'][idx])
                append_outburst = True
            if xb < umbral and append_outburst == True:
                inc_t_min = 1
                inc_t_max = 30
                all_ok = True
                activity_idx = 0
                print ('Length of Activity Block: %d' %len(activity_blocks))
                if len(activity_blocks) >= 3:                    
                    while all_ok and activity_idx < len(activity_blocks):                        
                        activity_weight = activity_blocks[activity_idx][1] - activity_blocks[activity_idx][0]
                        print ('initial_time: '+str(activity_blocks[activity_idx][0]))
                        print ('weight: '+str(activity_weight))
                        if activity_weight < inc_t_min or activity_weight > inc_t_max:
                            all_ok = False
                            print("=============================")
                        else:
                            activity_idx = activity_idx+1
                    
                    if all_ok:
                        outburst.append(1)
                        print ("Outbust Found")
                        print (activity_blocks[0][0])
                    activity_blocks = []
                else:
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
        #plt.plot(t_blocks, x_blocks) 
        #plt.plot(self.__lc[0],df_umbral)
        #plt.show()




if __name__ == '__main__':
    #myBlk = OurBayesianBlocks('maxi','Aql X-1')
    myBlk = AstropyBayesianBlocks('maxi','GS 0834-430 with GS 0836-429')
    #myBlk.getOutbursts()