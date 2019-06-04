import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, Legend, LegendItem
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import Viridis5


columns=['e1', 'e2', 'e3', 'pA Site', 'e4']
df = pd.read_csv('/Users/knaggert/Desktop/BioLab2019/dataVis/YSH1.fa.pos.txt', sep='\t', skiprows=1, header = None, names = ['Base', 'Position', 'e1', 'e2', 'e3', 'pA Site', 'e4'])

df = df.drop(columns=['Base','Position'])

# Convert from pandas dataframe to dictionary
    
data = ColumnDataSource(dict(
    x = [df.index]*len(columns),
    y = [df[column].values for column in columns],
    color=Viridis5))

TOOLS = "hover, save, pan, box_zoom, undo, redo, reset, wheel_zoom"
p = figure(sizing_mode = 'stretch_both', tools=TOOLS, tooltips = [('Position', '$x'), ('Score', '$y')])

ax = p.multi_line(source = data, xs = 'x', ys = 'y', line_width=2, line_color='color', line_alpha=0.6, hover_line_color='color', hover_line_alpha=1.0)

# Add in legend parameters

legend = Legend(items=[
    LegendItem(label="e1", renderers=[ax], index=0),
    LegendItem(label="e2", renderers=[ax], index=1),
    LegendItem(label="e3", renderers=[ax], index=2),
    LegendItem(label="pA Site", renderers=[ax], index=3),
    LegendItem(label="e4", renderers=[ax], index=4),
])

p.add_layout(legend)

# Label x and y-axis and give title

p.title.text = 'Interactive Plot Iteration 2.0'
p.xaxis.axis_label = 'Position'
p.yaxis.axis_label = 'Value'

show(p)
