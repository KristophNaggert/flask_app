from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.palettes import Viridis5
from bokeh.models import Legend, LegendItem, Range1d, HoverTool, RedoTool, UndoTool
from bokeh.embed import components

import pandas as pd
import numpy as np

data = pd.read_csv('YSH1.fa.pos.txt', sep='\t', skiprows=1, header = None, names = ['Base', 'Position', 'e1', 'e2', 'e3', 'pA Site', 'e4'])

array_1 = []

for k in range(len(data)):
    if (k+6 >= len(data)):
        array_1.append("N/A")
    else:
        s=""
        list1=[]
        for l in range(k, k+6):
            list1.append(data.Base[l])
        s=s.join(list1)
        array_1.append(s)

Sequences = pd.DataFrame(array_1, columns=['Sequence'])
df_complete = pd.concat([data, Sequences], axis = 1)

source = ColumnDataSource(df_complete)

TOOLS = "hover, save, pan, box_zoom, undo, redo, reset, wheel_zoom"

# e1
s1 = figure(title = 'e1', toolbar_location = "right", tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e1'), ('Sequence', '@Sequence')])
s1.line('Position', 'e1', line_width = 2, color = Viridis5[0], source = source)
s1.yaxis.axis_label = "Score"

# e2
s2 = figure(title = 'e2', x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e2'), ('Sequence', '@Sequence')])
s2.line('Position', 'e2', line_width = 2, color = Viridis5[1], source = source)
s2.yaxis.axis_label = "Score"

# e3
s3 = figure(title = 'e3',x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e3'), ('Sequence', '@Sequence')])
s3.line('Position', 'e3', line_width = 2, color = Viridis5[2], source = source)
s3.yaxis.axis_label = "Score"

# pA Site
s4 = figure(title = 'pA Site', x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@pA Site'), ('Sequence', '@Sequence')])
s4.line('Position', 'pA Site', line_width = 2, color = Viridis5[3], source = source)
s4.yaxis.axis_label = "Score"

# e4
s5 = figure(title='e4',x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e4'), ('Sequence', '@Sequence')])
s5.line('Position', 'e4', line_width = 2, color = Viridis5[4], source = source)
s5.yaxis.axis_label = "Score"

grid = gridplot([s1, s2, s3, s4, s5], ncols = 1, plot_height = 115, plot_width = 600, toolbar_location = 'right')
show(grid)

script, div = components(grid)
print(script)
print(div)
