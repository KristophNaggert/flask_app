from wtforms import Form, TextField, IntegerField, validators
from wtforms.validators import DataRequired, Optional


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
    upstream_buffer = IntegerField(label = 'Upstream Buffer', validators = [RequiredIf(gene='')], default=100)
    downstream_buffer = IntegerField(label = 'Downstream Buffer', validators = [RequiredIf(gene='')], default=500)


'''

Need to create checks to see if any of the fields were filled out, and if
gene_id or gene_name were submitted require the up and downstream buffer
queries to be filled.

0.) For some reason, upstream_buffer and downstream_buffer are not
being recognized and as such error when they are included . . . Something
to do with syntax.

1.) Is meant to check if either the input gene id or gene name exists
in the list of names/ids on SCD.
    Note: There must be a better way to check which fields have inputs

2.) Create a method that requires one of gene_id, gene_name or user_sequence
to have been filled out, and if gene_id or gene_name were filled in require
the user to input an up and downstream buffer.

'''

'''

1.)

    def validate_gene(form, field):
        if field.data.gene_id != NULL:
            if field.data.gene_id not in gene_list:
                raise ValidationError("We're sorry, input gene ID does not exist")
        else if field.data.gene_name != NULL:
            if field.data.gene_name not in gene_list:
                raise ValidationError("We're sorry, input gene name does not exist")
        else:

'''
