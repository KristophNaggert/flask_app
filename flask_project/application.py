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

        while (len(gene_from_genome)==0 & len(user_input_seq)==0):
            time.sleep(1)

        from getSeq import get_seq
        ret_seq = getSeq(upstreamBuf, downstreamBuf, gene_from_genome)
        print(ret_seq)



    return render_template('query.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
