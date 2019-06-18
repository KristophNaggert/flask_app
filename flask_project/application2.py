from flask import Flask, render_template, request
from wtforms import Form, TextField, validators
from wtforms.validators import DataRequired, Optional
import sys, time, requests

app = Flask(__name__)

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

        print(gene_from_genome)
        print(upstreamBuf)
        print(downstreamBuf)
        print(user_input_seq)

        time.sleep(20)

        global seq
        seq = get_seq(gene_from_genome, upstreamBuf, downstreamBuf)
        print(seq)

    return render_template('query.html', form = form, gene_from_genome = gene_from_genome, upstreamBuf = upstreamBuf, downstreamBuf = downstreamBuf, user_input_seq = user_input_seq, seq = seq)

def get_seq(gene_from_genome, upstreamBuf, downstreamBuf):
    '''
    Sourced from: https://rest.ensembl.org/documentation/info/sequence_id
    '''

    server = "https://rest.ensembl.org"

    ext = '/sequence/id/'+gene_from_genome+'?expand_5prime='+downstreamBuf+';expand_3prime='+upstreamBuf
    #print(ext)

    r = requests.get(server+ext, headers={ "Content-Type" : "text/plain"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    #print(r.text)
    seq = r.text

    return seq

if __name__ == '__main__':
    app.run(debug=True)
