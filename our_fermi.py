import params
import urllib.request

def obtener_periodos(p_html):
    return(float(p_html.replace('<td align=right>','').replace('<td align="right">','')))

def obtener_url(p_href):
    url = None
    if p_href != '<a></a>':
        ini_url = p_href.find('"')+1
        tag_aux = p_href[ini_url:]
        fin_url = tag_aux.find('"')
        url = tag_aux[:fin_url]
    return url
   
def tratar_tabla(p_tabla):
    tab = p_tabla
    tab = tab.replace('<table>','').replace('</table>','').replace("  ",'').replace('<tr>','').replace('<td>','').replace('<tr align=left>','')
    i = 0
    tr = 999
    l_sources = []
    tag = '</tr>'
    tr = tab.find(tag)+len(tag)
    while tr > 0:
        if i == 0:
            tab = tab[tr:]
            i=i+1
            tr = tab.find(tag)+len(tag)
        else:           
            tr  = tr+len(tag) 
            tab_aux = tab[0:tr]
            l_lna = tab_aux.split('</td>')
            ini_source = l_lna[0].find('">')+2
            tag_source = (l_lna[0][ini_source:].replace("</a>","")).replace('<td>','')
            if (tag_source.find("<a") >= 0):
                ini_tag = tag_source.find('>')
                tag_source = tag_source[ini_tag+1:]
            period1 = obtener_periodos(l_lna[1])
            period2 = obtener_periodos(l_lna[2])
            period3 = obtener_periodos(l_lna[3])
            url_sw = obtener_url(l_lna[4])
            url_maxi = obtener_url(l_lna[5])
            url_simb = obtener_url(l_lna[6])
            dict_source = {}
            dict_source['source'] = tag_source
            dict_source['period1'] = period1
            dict_source['period2'] = period2
            dict_source['perido3'] = period3
            dict_source['url_swift'] = url_sw
            dict_source['url_maxi'] = url_maxi
            dict_source['url_simbad'] = url_simb
            print (tag_source)
            l_sources.append(dict_source)
            tab = tab[tr:]
            tr = tab.find(tag)
    return l_sources

            


class Fermi:
    __url = params.url
    __db = params.db
    __client = params.client
    
    def __init__(self,id):
        fits = self.__db['parameters']
        rdo = fits.find_one(id)
        self.__url = rdo['url']

    def getUrl(self):
        return self.__url

    def readSources(self, p_url, tool_name):
        html = str(urllib.request.urlopen(p_url).read()).replace('\\n','').replace('\\t','').replace(" border=2",'')
        l_tables = []
        fin_table = 999
        while fin_table > 0:
            ini_table = html.find('<table>')
            fin_table = html.find('</table>')
            html_aux = 0
            if fin_table >= 0:
                html_aux = html[ini_table:fin_table+len('</table>')+len('</table>')]
                l_tables.append(html_aux)
                html = html[fin_table+len('</table>'):]
        
        for tab in l_tables:
            l_tables = l_tables+tratar_tabla(tab)
        
        sources = self.__db['sources']        
        dict_source = {'tool_name':tool_name,'sources':l_tables}
        sources.update({'tool_name':tool_name},dict_source, upsert=True)



