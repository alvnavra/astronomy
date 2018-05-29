import params
import urllib.request

def obtener_periodos(p_html):
    return(float(p_html.replace('<td align=right>','')))

def obtener_url(p_href):
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
    while tr > 0:
        tag = '</tr>'
        if i == 0:
            tr = tab.find(tag)+len(tag)
            tab = tab[tr:]
            i=i+1
        else:
            tr = tab.find(tag)+len(tag)
            tab_aux = tab[0:tr]
            l_lna = tab_aux.split('</td>')
            ini_source = l_lna[0].find('">')+2
            tag_surce = l_lna[0][ini_source:].replace("</a>","")
            period1 = obtener_periodos(l_lna[1])
            period2 = obtener_periodos(l_lna[2])
            period3 = obtener_periodos(l_lna[3])
            url_sw = obtener_url(l_lna[4])
            url_maxi = obtener_url(l_lna[5])
            url_simb = obtener_url(l_lna[6])
            dict_source = {}
            dict_source['source'] = tag_surce
            dict_source['period1'] = period1
            dict_source['period2'] = period2
            dict_source['perido3'] = period3
            dict_source['url_swift'] = url_sw
            dict_source['url_maxi'] = url_maxi
            dict_source['url_simbad'] = url_simb
            l_sources.a(dict_source)
    print(l_sources)

            


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
            tratar_tabla(tab)



