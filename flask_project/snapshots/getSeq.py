import requests, sys

'''
Sourced from: https://rest.ensembl.org/documentation/info/sequence_id
'''

class get_seq(upstreamBuf, downstreamBuf, gene_from_genome):

    server = "https://rest.ensembl.org"

    ext = '/sequence/id/'+gene_from_genome+'?expand_5prime='+downstreamBuf+';expand_3prime='+upstreamBuf
    print(ext)

    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    print(r.text)
    seq = r.text
