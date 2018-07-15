import params
import urllib.request

class Maxi:
    __url = params.url
    __db = params.db
    __client = params.client

    def __init__(self,id):
        db = self.__db['parameters']
        rdo = db.find_one(id)
        self.__url = rdo['urls'][0]['sources_list']

    def getUrl(self):
        return self.__url

    def returnTypes(self, p_url):
        sources = self.__db['sources']
        html = str(urllib.request.urlopen(p_url).read()).replace('\\n','')
        tr = html.find('<tr>')
        html_aux = ''
        fin_tag = 0
        i = 0
        while (tr >= 0):
            if i==0:
                ini_tag = tr+len('<tr>')
                html_aux = html[ini_tag:]
                fin_tag = html_aux.find('</tr>')+len('</tr>')
                html_aux = html_aux[fin_tag:]
                i = i+1
            else:
                ini_tag = tr+len('<tr>')
                fin_tag = ini_tag+html_aux.find('</tr>')+len('</tr>')
                lna_aux = html_aux[ini_tag:fin_tag]
                ini_tag = lna_aux.find('</th>')+len('</th>')
                l_lna = lna_aux[ini_tag:].split('</td>')

                if len(l_lna) == 1 and l_lna[0] == '':
                    tr = -1
                    continue

                source_ini = l_lna[0].find('">')+2
                source_fin = l_lna[0][source_ini:].find('</a>')
                source = (l_lna[0][source_ini:source_ini+source_fin]).strip()
                print(source)
                '''if source == 'QSO B2356-309':
                    print(source)'''

                str_ra_obj = l_lna[1].replace('<td align=right>','').strip()
                str_dec_obj = l_lna[2].replace('<td align=right>','').strip()
                str_lii_obj = l_lna[3].replace('<td align=right>','').strip()
                str_bii_obj = l_lna[4].replace('<td align=right>','').strip()


                type_src = l_lna[5].replace('<td>','').replace('\n','').strip()
                if source.find(',') < 0:
                    query = {'tool_name':'maxi','source':source}
                    url_base_lc = 'http://maxi.riken.jp/star_data/'
                    dict_source = sources.find_one(query)
                    if dict_source == None:
                        dict_source = {}
                        dict_source['source'] = source
                        dict_source['tool_name'] = 'maxi'
                                          
                    dict_source['src_type'] = type_src
                    dict_source['ra_obj'] = float(str_ra_obj)
                    dict_source['dec_obj'] = float(str_dec_obj)
                    dict_source['LII'] = float(str_lii_obj)
                    dict_source['BII'] = float(str_bii_obj)
                    url_lc = url_base_lc+source+'/'+source
                    dict_lc_urls = {'daily':url_lc+'_g_lc_1day_all.dat','orbital':url_lc+'_g_lc_1orb_all.dat'}
                    dict_source['ligth_curves'] = dict_lc_urls

                    sources.update(query,dict_source,upsert=True)
                else:
                    l_names = source.split(',')
                    for  name in l_names:
                        query = {'tool_name':'maxi','source':name}
                        dict_source = sources.find_one(query)
                        if dict_source == None:
                            dict_source = {}
                            dict_source['source'] = name
                            dict_source['tool_name'] = 'maxi'
                            url_base_lc = 'http://maxi.riken.jp/star_data/'
                        if len(dict_source) > 0:
                            dict_source['src_type'] = type_src
                            dict_source['ra_obj'] = float(str_ra_obj)  
                            dict_source['dec_obj'] = float(str_dec_obj)    
                            dict_source['LII'] = float(str_lii_obj)  
                            dict_source['BII'] = float(str_bii_obj)  
                            url_lc = url_base_lc+source+'/'+source
                            dict_lc_urls = {'daily':url_lc+'_g_lc_1day_all.dat','orbital':url_lc+'_g_lc_1orb_all.dat'}
                            dict_source['ligth_curves'] = dict_lc_urls
                  
                            sources.update(query,dict_source,upsert=True)
                            break



                    
                html_aux = html_aux.replace(lna_aux,'')
            tr = html_aux.find('<tr>')
            
        

    def readSources(self, p_url, tool_name):
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
                    source = l_aux[0].replace('\\n<td>','').replace('<td>','')
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
                    dict_source = {'source':source,'url':url,'url_1_orb':url_lc_1orb,'url_1_day':url_lc_1day,'tool_name':tool_name}
                    sources = self.__db['sources']
                    sources.update({'source':source},dict_source,upsert=True)

    def readTypes(self, p_tool_name):
        parameters = self.__db['parameters']
        sources_types_url = parameters.find_one({'_id':p_tool_name},{'urls':1,'_id':0})['urls'][0]['sources_info']
        for url in sources_types_url:
            self.returnTypes(url)


        '''sources = self.__db['sources']        
        dict_source = {'tool_name':tool_name,'sources':l_sources}
        sources.update({'tool_name':tool_name},dict_source, upsert=True)'''

if __name__ == '__main__':
    maxi = Maxi('maxi')
    maxi.readTypes('maxi')
    maxi.readSources('http://maxi.riken.jp/star_data/','maxi')
