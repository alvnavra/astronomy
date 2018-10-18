from astroquery.simbad import Simbad
result_table = Simbad.query_objectids("Polaris")
x = [r['ID'] for r in result_table]
print(x)
'''for reg in result_table:
    print (reg['ID'])'''
#print(result_table)
#print (str(result_table).replace('\n',''))
