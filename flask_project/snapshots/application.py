from model import InputForm
from flask import Flask, render_template, request
import sys, time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        gene_from_genome = form.gene.data
        upstreamBuf = form.upstream_buffer.data
        downstreamBuf = form.downstream_buffer.data
        user_input_seq = form.sequence.data

        print(gene_from_genome)
        print(upstreamBuf)
        print(downstreamBuf)
        print(user_input_seq)

        time.sleep(20)

        while (len(gene_from_genome)==0 and len(user_input_seq)==0):
            time.sleep(1)

    return render_template('query.html', form=form)

from getSeq import get_seq

def retreive_sequence(upstreamBuf, downstreamBuf, gene_from_genome):

    ret_seq = get_seq(upstreamBuf, downstreamBuf, gene_from_genome)

    return ret_seq

if __name__ == '__main__':
    app.run(debug=True)
