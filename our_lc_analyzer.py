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

    def getClasif(self, p_mission, p_source, p_regs=3):
        print ("Clasificando: "+p_source)
        myBayesian = OurBayesianBlocks()
        myBayesian.calculate_bayesian_blocks(p_mission, p_source)
        threshold = myBayesian.getThreshold()
        self.__lc = myBayesian.getLightCurve()
        df = self.__lc
        last = df[1].iloc[-1]
        nextToLast = df[1].iloc[-2]
        secondToLast= df[1].iloc[-3]
        activity = myBayesian.hasActivity()
        '''Eliminamos la variable booleana 'activity' pk no tiene sentido.
           No tener actividad, significa actividad 0 (o -1 si no se ha informado
           previamente). Que es menor que 100 (en ambos casos), por lo tanto, 
           eliminamos el control'''
        if myBayesian.getActivity() < 100:
            if secondToLast <  nextToLast < last :
                activityPercentage = 0
                if last > threshold :
                    activityPercentage = 25
                    if nextToLast > threshold :
                        activityPercentage = 50
                        if secondToLast > threshold :
                            activityPercentage= 75
                myBayesian.setActivity(activityPercentage)
            else:
                myBayesian.setActivity(0)
                   
        if myBayesian.getActivity() == 100 :
            if last < threshold and secondToLast < threshold :
                myBayesian.setActivity(0)       

    
if __name__ == '__main__':

    myAnalyzer = OurLCAnalyzer()
    myAnalyzer.getClasif('swift','QSO B0003-066')






