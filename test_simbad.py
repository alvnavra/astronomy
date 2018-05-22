from astroquery.simbad import Simbad
result_table = Simbad.query_objectids("Polaris")
print(result_table)
