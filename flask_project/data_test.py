''' Import Libraries'''

import pandas as pd
import numpy as np
import sys

''' Read in the data '''
''' Path to data currently hard coded, needs will need to changed when moved to server '''

df = pd.read_csv('/Users/knaggert/Desktop/flask_project/data/results.tsv', delimiter=r'\s+', header = None, names = ['Sys_Name','Std_Name'])

gene = sys.argv[1]
print(gene)
gene = gene.upper()
print(gene)

if (any(df['Sys_Name'] == gene)):
    gene = gene
    print(gene)
else:
    index = next(iter(df[df.Std_Name==gene].index), 'No match.')
    print (index)
    gene = df.Sys_Name[index]
    print(gene)
