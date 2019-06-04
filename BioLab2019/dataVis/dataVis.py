# Data Visualization Program
# Kristoph Naggert
# May 20th, 2019
# Package : Seaborn

# Read in Dataframe from .txt file #

import pandas as pd
data = pd.read_csv('YSH1.fa.pos.txt', sep='\t', skiprows=1, header = None, names = ['Base', 'Position', 'e1', 'e2', 'e3', 'pA Site', 'e4'])

# Convert to format for Seaborn #

data_preproc = pd.DataFrame({
    'Position' : data['Position'],
    'e1' : data['e1'],
    'e2' : data['e2'],
    'e3' : data['e3'],
    'pA Site' : data['pA Site'],
    'e4' : data['e4']})


# Set up for Seaborn #

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
sns.set(style="darkgrid")


# Set color palette #

colors = ['#243485', '#572b9f', '#9537a1', '#d05379', '#ff7552'] 

# Lineplot and Figure Aesthetics in Seaborn #

sns.set_context(rc={"lines.linewidth":0.75})
ax = sns.lineplot(x = "Position", y = "value", hue = "variable", palette = sns.color_palette(colors), data = pd.melt(data_preproc, ['Position']))
# ax.set() # xlabel, ylabal and title
plt.show()
