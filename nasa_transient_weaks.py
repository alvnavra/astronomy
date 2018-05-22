class nTransientWeaks:
    __l_files = []
    def __init__(self,html):
        html_aux = html
        ini_table = html_aux.find('<table border=2>')
        html_aux = html_aux[ini_table:]
        ini_table = 0
        fin_lna = 0
        fin_table = html_aux.find('</table>')
        html_aux = html_aux[ini_table:fin_table]
        i = 1
        while html_aux != '':
            ini_lna = html_aux.find('<a href="')+len('<a href="')
            fin_lna = html_aux.find('">')
            if fin_lna != -1:
                href = html_aux[ini_lna:fin_lna]
                html_aux = html_aux[fin_lna+1:]
                self.__l_files.append(href)
                if i%100 == 0:
                    print ("Tratando columna %d" %i)
                i = i+1
            else:
                html_aux = ''
        print ("%d Columnas Tratadas" %(i-1))


    def getFiles(self):
        return self.__l_files


        