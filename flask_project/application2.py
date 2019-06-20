'''
----------------------------------------------------------------------------------
|             application2.py - Data visualization Flask application             |
----------------------------------------------------------------------------------
| Kristoph Naggert | Mount Desert Island Biological Laboratory | Oberlin College |
----------------------------------------------------------------------------------
|                           Friday, June 18th, 2019                              |
----------------------------------------------------------------------------------
'''

'''
Import required libraries and specific functions.
'''

from flask import Flask, render_template, request
from wtforms import Form, TextField, validators
from wtforms.validators import DataRequired, Optional
import sys, time, requests
import pandas as pd
import numpy as np

app = Flask(__name__)


'''
Initialize Global Varaibles
'''

gene_from_genome = ""
upstreamBuf = ""
downstreamBuf = ""
user_input_seq = ""
seq = ""



class RequiredIf(DataRequired):

    '''
    Validator which makes a field required if another field is set and has a truthy value.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    '''

    field_flags = ('requiredif',)

    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    # field is requiring that name field in the form is data value in the form
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)



class InputForm(Form):
    gene = TextField(label = 'Enter Standard Yeast Gene ID or Gene Name', validators = [validators.optional()])
    sequence = TextField(label = 'Specific User Generated Gene Sequence', validators = [RequiredIf(gene='')])
    upstream_buffer = TextField(label = 'Upstream Buffer', validators = [RequiredIf(gene='')], default='100')
    downstream_buffer = TextField(label = 'Downstream Buffer', validators = [RequiredIf(gene='')], default='500')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():

        global gene_from_genome
        global upstreamBuf
        global downstreamBuf
        global user_input_seq

        gene_from_genome = form.gene.data
        upstreamBuf = form.upstream_buffer.data
        downstreamBuf = form.downstream_buffer.data
        user_input_seq = form.sequence.data

        '''
        Need to come up with a useable solution here.
        '''

        time.sleep(15) '''This will need to be changed in the final iteration of the application'''

        gene_from_genome = convert_to_symbol(gene_from_genome)

        global seq
        seq = get_seq(gene_from_genome, upstreamBuf, downstreamBuf)
        print(seq)

        '''
        Run the predictive program with the fetched or user inputed sequence.

        pred_out = predict(seq) #Probabily need to turn this into a global variable.
        '''

        '''
        Pass that predictive output into the data visualization tools.
        '''

        '''
        Build in a reset function, so that the page doesn't need to be reloaded
        each time a plot is created and the user wants to display new ones.
        Potential solutions to this would be to:

        1.) Host the data visualizations on a different page (That is submiting
        user inputs redirects the user to a webpage extension).

        2.) Build a reset button that clears all inputs and resets all variables,
        allowing the user to re-run with new inputs.
        '''

    return render_template('query.html', form = form, gene_from_genome = gene_from_genome, upstreamBuf = upstreamBuf, downstreamBuf = downstreamBuf, user_input_seq = user_input_seq, seq = seq)



def get_seq(gene_from_genome, upstreamBuf, downstreamBuf):

    '''
    Sourced from: https://rest.ensembl.org/documentation/info/sequence_id
    '''

    server = "https://rest.ensembl.org"

    ext = '/sequence/id/'+gene_from_genome+'?expand_5prime='+downstreamBuf+';expand_3prime='+upstreamBuf

    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    seq = r.text

    return seq



def convert_to_symbol(gene_from_genome):

    ''' Read in the data '''
    ''' Path to data currently hard coded, needs will need to changed when moved to server '''

    df = pd.read_csv('/Users/knaggert/Desktop/flask_project/data/results.tsv', delimiter=r'\s+', header = None, names = ['Sys_Name','Std_Name'])

    gene_from_genome = gene_from_genome.upper()

    if (any(df['Sys_Name'] == gene_from_genome)):
        gene_from_genome = gene_from_genome
        return gene_from_genome
    else:
        index = next(iter(df[df.Std_Name==gene_from_genome].index), 'No match.')
        gene_from_genome = df.Sys_Name[index]
        return gene_from_genome

    '''
    Currently has no way to catch and inform the user of the application
    if the standard gene name or systematic gene name do not exist in the
    local database.

    Also need to create a catch if there is no input, becuase there are certain
    entries in the gene list (results.tsv) whose Std_Name entry is ""and the
    application might break if the program tries to find the gene name "" when a
    user sequence is input.
    '''


if __name__ == '__main__':
    app.run(debug=True)
