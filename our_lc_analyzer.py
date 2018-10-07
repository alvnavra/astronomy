import params
import pandas as pd
import numpy as np
from our_bayesian_blocks import OurBayesianBlocks
from io import StringIO

class OurLCAnalyzer:
    __url = params.url
    __db = params.db
    __client = params.client
    __lc = None

    def getClasif(self, p_tool_name, p_source, p_regs=3):
        myBayesian = OurBayesianBlocks()
        myBayesian.calculate_bayesian_blocks(p_tool_name, p_source)
        threshold = myBayesian.getThreshold()
        self.__lc = myBayesian.getLightCurve()
        df = self.__lc
        last = df[1].iloc[-1]
        nextToLast = df[1].iloc[-2]
        secondToLast= df[1].iloc[-3]
        activity = myBayesian.hasActivity()
        if activity == False or myBayesian.getActivity() < 100:
            if secondToLast <  nextToLast < last :
                activityPercentage = 25
                if last > threshold :
                    activityPercentage = 50
                    if nextToLast > threshold :
                        activityPercentage = 75
                        if secondToLast > threshold :
                            activityPercentage= 100
                myBayesian.setActivity(activityPercentage)
                activity = True
                   
        if myBayesian.getActivity() == 100 :
            if last < threshold and secondToLast < threshold :
                activity = False        

    
if __name__ == '__main__':

    myAnalyzer = OurLCAnalyzer()
    myAnalyzer.getClasif('swift','QSO B0003-066')






