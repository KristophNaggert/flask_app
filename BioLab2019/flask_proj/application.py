from flask import Flask, render_template

app = Flask(__name__)

# Load in required libraries

import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, Legend, LegendItem
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

@app.route('/')
def interactiveplot():

    hover = create_hover_tool()
    plot = multilineplot(hover)

    script, div = components(plot)
    print(script)
    print(div)
    
    return render_template("chart.html", div=div, script=script)


def create_hover_tool():
    # we'll code this function in a moment
    return None

def multilineplot(hover_tool=None):
    
    columns=['e1', 'e2', 'e3', 'pA Site', 'e4']
    df = pd.read_csv('/Users/knaggert/Desktop/BioLab2019/dumb/data/YSH1.fa.pos.txt', sep='\t', skiprows=1, header = None, names = ['Base', 'Position', 'e1', 'e2', 'e3', 'pA Site', 'e4'])

    df = df.drop(columns=['Base','Position'])

    # Convert from pandas dataframe to dictionary
    
    data = ColumnDataSource(dict(
    x=[df.index]*len(columns),
    y=[df[column].values for column in columns],
    color=['red','blue','green','orange','purple']))

    p = figure()

    ax = p.multi_line(source=data, xs='x', ys='y', color='color')

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

    return p

if __name__ == "__main__":
    app.run(debug=True)
