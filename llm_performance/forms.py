from django.forms import forms, fields, widgets


def encode_ascii_for_list_of_strings(values):
    for value in values:
        if isinstance(value, str):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                raise forms.ValidationError('Please use only English characters')
    return True


class ReportSendForm(forms.Form):

    name = fields.CharField(
        label='user name:',
        disabled=True,
    )

    email = fields.CharField(
        label='e-mail:',
        disabled=True,
    )

    cpu = fields.CharField(
        label='CPU model name:',
        help_text='',
    )

    gpu = fields.CharField(
        label='GPU model name:',
        help_text='',
    )

    message = fields.CharField(
        label='command output (copy & paste from the terminal):',
        widget=widgets.Textarea(attrs={
            'rows': 20,
            'style': 'font-family: monospace;',
            'placeholder': '''user@localhost:~$ ollama run llama2 --verbose
>>> tell me a joke!

Sure, here's a classic one:

Why don't scientists trust atoms?
Because they make up everything!

I hope that made you smile!

total duration:       35.953439268s
load duration:        15.629763ms
prompt eval count:    27 token(s)
prompt eval duration: 12.890555s
prompt eval rate:     2.09 tokens/s
eval count:           39 token(s)
eval duration:        23.039657s
eval rate:            1.69 tokens/s''',
        })
    )

    duplicate = fields.BooleanField(
        label='send me a copy of this report',
        initial=True,
    )

    def clean(self):
        cleaned_data = super(ReportSendForm, self).clean()
        encode_ascii_for_list_of_strings(cleaned_data.values())
        return cleaned_data
