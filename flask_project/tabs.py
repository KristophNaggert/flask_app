'''
----------------------------------------------------------------------------------
|   tabs.py - Program that displays visual representation of yeast PolyA data    |
----------------------------------------------------------------------------------
| Kristoph Naggert | Mount Desert Island Biological Laboratory | Oberlin College |
----------------------------------------------------------------------------------
|                            Friday, June 7th, 2019                              |
----------------------------------------------------------------------------------
'''


''' Import General Libraries '''

import sys
from math import pi
import numpy as np
import pandas as pd


''' Import Bokeh Functions '''

from bokeh.io import show
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, ContinuousTicker
from bokeh.models import Legend, LegendItem, Range1d, HoverTool, RedoTool, UndoTool
from bokeh.models.widgets import Tabs, Panel
from bokeh.embed import components
from bokeh.layouts import layout, widgetbox, column, row, gridplot
from bokeh.palettes import Viridis5, Magma256

''' Import Flask Functions [Eventually] '''

def Intensity_Plot(data, TOOLS):

    dataI = data
    
    columns = ['e1', 'e2', 'e3', 'pASite', 'e4']

    array_1 = []

    for k in range(len(dataI)):
        if (k+6 >= len(dataI)):
            array_1.append("N/A")
        else:
            s = ""
            list1 = []
            for l in range(k, k+6):
                list1.append(dataI.Base[l])
            s = s.join(list1)
            array_1.append(s)

    sequences = []
    for n in range(len(dataI)*len(columns)):
        sequences.append(n)

    temporary = 0
    for q in range(len(array_1)):
        for d in range(len(columns)):
            sequences[temporary] = array_1[q]
            temporary = temporary+1

    Sequences = pd.DataFrame(sequences, columns = ['Sequence'])

    dataI['Position'] = dataI['Position'].astype(str)
    dataI = dataI.set_index('Position')

    dataI = dataI.drop(columns = ['Base'])

    dataI.columns.name = 'Values'
    Position = list(dataI.index)
    Position = list(map(int, Position))
    Values = list(dataI.columns)

    df_I = pd.DataFrame(dataI.stack(), columns = ['score']).reset_index()

    df_complete = pd.concat([df_I, Sequences], axis = 1)


    Magma256.reverse()
    mapper = LinearColorMapper(palette = Magma256, high = df_complete.score.max(), low = df_complete.score.min())

    p = figure(title = "Heatmap of Sites", x_range = (0,len(Position)), y_range = Values,
               x_axis_location = "above", sizing_mode = 'stretch_both',
               tools = TOOLS, toolbar_location = 'below',
               tooltips = [('Position','@Position'), ('Score', '@score'), ('Sequence', '@Sequence')])



    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3

    p.rect(x = 'Position', y = 'Values', width = 1, height = 1,
           source = df_complete,
           fill_color = {'field':'score', 'transform' : mapper},
           line_color = None)

    color_bar = ColorBar(color_mapper = mapper, major_label_text_font_size = "10pt",
                         ticker = BasicTicker(),
                         label_standoff = 6, border_line_color = None, location = (0, 0))

    p.add_layout(color_bar, 'right')

    script_heat, div_heat = components(p)

    return(p)

    
def Stacked_Line_Plot(data, TOOLS):

    dataS = data
    
    '''
    Stacked Plots (Left-Hand Side)
    '''

    array = []

    for k in range(len(dataS)):
        if (k+6 >= len(dataS)):
            array.append("N/A")
        else:
            s = ""
            list_1 = []
            for l in range(k, k+6):
                list_1.append(dataS.Base[l])
            s = s.join(list_1)
            array.append(s)

    Seq = pd.DataFrame(array, columns = ['Seq'])
    df_comp = pd.concat([dataS, Seq], axis = 1)

    source = ColumnDataSource(df_comp)

    ''' Individual Line Graph for  e1 '''
    
    s1 = figure(title = 'e1', toolbar_location = "right", tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e1'), ('Sequence', '@Seq')])
    
    s1.line('Position', 'e1', line_width = 2, color = Viridis5[0], source = source)
    
    s1.yaxis.axis_label = "Score"

    ''' Individual Line Graph for  e2 '''
     
    s2 = figure(title = 'e2', x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e2'), ('Sequence', '@Seq')])
    
    s2.line('Position', 'e2', line_width = 2, color = Viridis5[1], source = source)
    
    s2.yaxis.axis_label = "Score"

    ''' Individual Line Graph for  e3 '''
    
    s3 = figure(title = 'e3',x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e3'), ('Sequence', '@Seq')])
    
    s3.line('Position', 'e3', line_width = 2, color = Viridis5[2], source = source)
    
    s3.yaxis.axis_label = "Score"

    ''' Individual Line Graph for  pA Site '''
    
    s4 = figure(title = 'pA Site', x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS,
                tooltips = [('Position', '@Position'), ('Score', '@pASite'), ('Sequence', '@Seq')])
    
    s4.line('Position', 'pASite', line_width = 2, color = Viridis5[3], source = source)
    
    s4.yaxis.axis_label = "Score"

    ''' Individual Line Graph for  e4 '''
     
    s5 = figure(title='e4',x_range = s1.x_range, y_range = s1.y_range, tools = TOOLS, tooltips = [('Position', '@Position'), ('Score', '@e4'), ('Sequence', '@Seq')])
    
    s5.line('Position', 'e4', line_width = 2, color = Viridis5[4], source = source)
    
    s5.yaxis.axis_label = "Score"

    '''
    Multi-Line Plot (Right Hand Side)
    '''

    columns = ['e1', 'e2', 'e3', 'pASite', 'e4']
    dat = data
    dat = dat.drop(columns=['Base','Position'])

    # Convert from pandas dataframe to dictionary

    data2 = ColumnDataSource(dict(x = [dat.index]*len(columns),
                                  y = [dat[column].values for column in columns],
                                  color = Viridis5))
    p = figure()

    ax = p.multi_line(source = data2, xs = 'x', ys = 'y', line_width = 2, line_color = 'color', line_alpha = 0.6)

    legend = Legend(items = [
        LegendItem(label = "e1", renderers = [ax], index = 0),
        LegendItem(label = "e2", renderers = [ax], index = 1),
        LegendItem(label = "e3", renderers = [ax], index = 2),
        LegendItem(label = "pA Site", renderers = [ax], index = 3),
        LegendItem(label = "e4", renderers = [ax], index = 4),
    ])

    p.add_layout(legend)

    p.title.text = 'Multiline Plot'
    p.xaxis.axis_label = 'Position'
    p.yaxis.axis_label = 'Score'

    '''
    Layout
    '''

    l = layout(
        children = [
            [s1, s2, s3, s4, s5],
            [p]
        ],
        sizing_mode = 'stretch_both',
    )

    script_line, div_line = components(l)

    return(l)

def main():
    
    data_file = sys.argv[1]
    raw_data = pd.read_csv(data_file, sep = '\t', skiprows = 1, header = None, names = ['Base', 'Position', 'e1', 'e2', 'e3', 'pASite', 'e4'])
    TOOLS = "hover, save, pan, box_zoom, undo, redo, reset, wheel_zoom"

   #c output_file('Data-Visualization-Layout.html', title = '')
    
    lineplot = Stacked_Line_Plot(raw_data, TOOLS)    
    heatmap = Intensity_Plot(raw_data, TOOLS)

    first_panel = Panel(child = lineplot, title = 'Line Plot')
    second_panel = Panel(child = heatmap, title = 'Heatmap')

    tabs = Tabs(tabs = [first_panel, second_panel])

    show(tabs)

if __name__ == "__main__":
    main()
