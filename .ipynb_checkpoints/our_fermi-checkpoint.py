import params
import urllib.request

def tratar_tabla(p_tabla):
    tab = p_tabla
    tab = tab.replace('<table>','').replace('</table>','').replace("  ",'').replace('<tr>','').replace('<td>','').replace('<tr align=left>','')
    i = 0
    tr = 999
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
            pass
            


class Fermi:
    __url = params.url
    __db = params.db
    __client = params.client
    
    def __init__(self,id):
        fits = self.__db['missions']
        rdo = fits.find_one(id)
        self.__url = rdo['url']

    def getUrl(self):
        return self.__url

    def readSources(self, p_url, mission):
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



