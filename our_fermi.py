import params
import urllib.request
from astroquery.simbad import Simbad

def obtener_periodos(p_html):
    return(float(p_html.replace('<td align=right>','').replace('<td align="right">','')))

def obtener_url(p_href):
    url = None
    name = None
    if p_href != '<a></a>':
        ini_url = p_href.find('"')+1
        tag_aux = p_href[ini_url:]
        fin_url = tag_aux.find('"')
        url = tag_aux[:fin_url]
        name = tag_aux[fin_url:tag_aux.find("</a>")].replace('">',"")
    return url,name

def findSimbd(p_SimbId):
    customSimbad = Simbad()
    customSimbad.add_votable_fields('otype')
    error = True
    result_table = None
    while error:
        try:
            result_table = customSimbad.query_object(p_SimbId)
            rdo = str(result_table['OTYPE']).replace("  OTYPE   \n----------\n",'').replace("OTYPE\n-----\n ",'').replace("OTYPE \n------\n",'')
            return rdo
        except:
            pos_mas = p_SimbId.find('+')
            if pos_mas == -1:
                return None
            p_SimbId = p_SimbId.replace("+"," ",1)
            error = True
   
def tratar_tabla(p_tabla, p_mission, p_collection):
    #p_collection.drop({}) #Muy importante!!!!!! Esta línea se tiene que ejecutar en la primera fuente que se baje.
    swift = p_collection.find({'mission':'swift','source':'GX 1+4'})
    tab = p_tabla
    tab = tab.replace('<table>','').replace('</table>','').replace("  ",'').replace('<tr>','').replace('<td>','').replace('<tr align=left>','')
    i = 0
    tr = 999
    l_sources = []
    tag = '</tr>'
    tr = tab.find(tag)+len(tag)
    haveFits = False
    while tr > 0:
        if i == 0:
            tab = tab[tr:]
            i=i+1
            tr = tab.find(tag)+len(tag)
        else:
            haveFits = True           
            tr  = tr+len(tag) 
            tab_aux = tab[0:tr]
            l_lna = tab_aux.split('</td>')
            ini_source = l_lna[0].find('">')
            if ini_source >= 0:
                ini_source = ini_source+2
                tag_source = (l_lna[0][ini_source:].replace("</a>","")).replace('<td>','')
                if (tag_source.find("<a") >= 0):
                    ini_tag = tag_source.find('>')
                    tag_source = tag_source[ini_tag+1:]
            else:
                tag_source = l_lna[0]
            period1 = obtener_periodos(l_lna[1])
            period2 = obtener_periodos(l_lna[2])
            period3 = obtener_periodos(l_lna[3])
            name_sw, url_sw = obtener_url(l_lna[4])
            name_maxi, url_maxi = obtener_url(l_lna[5])
            url_simb,name_simb = obtener_url(l_lna[6])
            dict_source = {}
            dict_source['source'] = tag_source
            dict_source['LII'] = period1
            dict_source['BII'] = period2
            dict_source['period'] = period3
            dict_source['url_swift'] = url_sw
            dict_source['url_maxi'] = url_maxi
            dict_source['url_simbad'] = url_simb
            dict_source['simbad_id'] = name_simb
            dict_source['src_type'] = findSimbd(name_simb)
            dict_source['mission']=p_mission

            if haveFits == True:
                url_base = 'https://gammaray.nsstc.nasa.gov/gbm/science/pulsars/lightcurves/'
                src_base = dict_source['source'].replace(' ','').replace('+','p')
                url_fits = (url_base+src_base+'.fits.gz').lower()
                dict_source['ligth_curves'] = [url_fits]

            p_collection.update({'mission':p_mission,'source':tag_source},dict_source,upsert=True)
            tab = tab[tr:]
            tr = tab.find(tag)

            
class Fermi:
    __url = params.url
    __db = params.db
    __client = params.client
    
    def __init__(self,id):
        fits = self.__db['missions']
        rdo = fits.find_one(id)
        self.__url = rdo['urls'][0]['sources']

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
            tratar_tabla(tab, mission, self.__db['sources'])


if __name__ == '__main__':
    mission = 'fermi'
    my_fermi = Fermi(mission)
    url = my_fermi.getUrl()
    my_fermi.readSources(url,mission)
