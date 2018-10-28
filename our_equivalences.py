import params

class SourcesEquivalences:
    
    __db = None
    __client = None
    __orig_mission = None
    __equiv_mission = None

    def __init__(self):
        self.__db = params.db
        self.__client = params.client
        self.__orig_mission = 'swift'
        self.__equiv_mission = 'maxi'

    '''
        swift       maxi        source_swift    source_maxi
        GX+14       GX14        GX+14           GX14
        GX+14       MRK+56      GX+14           GX14
        GX+14       Sirus25     GX+14           GX14
        FSU900      GX14        GX+14           GX14
        X45                     X45
    '''

    def compare(self, p_so, p_se):
        so = p_so.upper().replace('MAXI','')
        se = p_se.upper().replace('SWIFT','')
        if so == se:
            return True
        return False

    def getEquivalences(self):

        db = self.__db
        sources = db['sources']
        sources_orig = sources.find({'mission':self.__orig_mission,'alt_names':{'$exists':True}},{'alt_names':1,'source':1,'_id':0})
        sources_equiv = sources.find({'mission':self.__equiv_mission,'alt_names':{'$exists':True}},{'alt_names':1,'source':1,'_id':0})

        for so in sources_orig:
            for se in sources_equiv:
                if so['alt_names']!=None and se['alt_names']!=None:
                    so_alt = so['alt_names']
                    se_equiv = se['alt_names']
                    for soa in so_alt:
                        for seq in se_equiv:
                            if self.compare(soa, seq) == True:
                                print('Hemos encontrado equivalencias')
                else:
                    break
                    


if __name__ == '__main__':
    sEquiv = SourcesEquivalences()
    sEquiv.getEquivalences()
