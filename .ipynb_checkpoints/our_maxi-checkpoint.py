import params
import urllib.request

class Maxi:
    __url = params.url
    __db = params.db
    __client = params.client

    def __init__(self,id):
        db = self.__db['missions']
        rdo = db.find_one(id)
        self.__url = rdo['url']

    def getUrl(self):
        return self.__url

    def readSources(self, p_url, mission):
        html = str(urllib.request.urlopen(p_url).read()).replace('\\n','')
        i = 0
        l_sources = []
        tr = 999
        while tr >= 0:
            tag = '</tr>'
            tr = html.find(tag)
            if tr >= 0:
                if i == 0:
                    html = html[tr+len(tag):]
                    i = i+1
                else:
                    html_aux = html[0:tr].replace('<tr>','').replace('</td>','').replace('align="center"',"")
                    l_aux = html_aux.split("<td >")
                    source = l_aux[0].replace('\\n<td>','')
                    href = l_aux[2].replace('<a href="','')
                    fin_ref = href.find('.html')+len('.html')
                    href = href[0:fin_ref].replace('..','')
                    root_href = p_url[0:p_url.find('/top')]
                    url = root_href+href
                    url_lc_1orb = url.replace('.html','_g_lc_1orb_all.dat')
                    url_lc_1day = url.replace('.html','_g_lc_1day_all.dat')
                    '''Comentada para más adelante. No eliminar'''
                    '''urllib.request.urlretrieve(url_lc_1day,'download.txt')
                    f = open('download.txt','rt')
                    buff = f.readlines()
                    for b in buff:
                        l_linea = b.split(' ')
                        print(l_linea)

                    exit(0)'''
                    html = html[tr+len(tag):]
                    print(l_aux)
                    print(source)
                    print(href)
                    print(p_url)
                    print(url)
                    print(url_lc_1day)
                    print(url_lc_1orb)
                    dict_source = {'source':source,'url':url,'url_1_orb':url_lc_1orb,'url_1_day':url_lc_1day}
                    l_sources.append(dict_source)
        
        sources = self.__db['sources']        
        dict_source = {'mission':mission,'sources':l_sources}
        sources.update({'mission':mission},dict_source, upsert=True)
                