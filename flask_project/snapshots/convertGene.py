import requests, sys

'''
Sourced from: https://rest.ensembl.org/documentation/info/symbol_lookup
'''

class convert_to_symbol():
    server = "https://rest.ensembl.org"
    #ext = "/lookup/symbol/saccharomyces_cerevisiae/GCN3?"

    gene = 'GCN3'
    ext = '/lookup/symbol/saccharomyces_cerevisiae/'+gene_from_genome+'?'

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not r.ok:
      r.raise_for_status()
      sys.exit()

    decoded = r.json()
    print(repr(decoded['id']))
    gene_sym = (repr(decoded['id']))
