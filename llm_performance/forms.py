# -*- coding: UTF-8 -*-

import re

from django.forms import forms, fields, widgets


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
        help_text='here you enter full model name of your Central Processor',
    )

    gpu = fields.CharField(
        label='GPU model name:',
        help_text='enter here details about your Graphics Processing Unit model',
    )

    message = fields.RegexField(
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
        }),
        regex=re.compile(
            pattern='^.*?ollama.+\-\-verbose.+'
                    'total duration\:\s+?(?P<total_duration>[\d\.ywduhmnsµμ]+)\s+'
                    'load duration\:\s+?(?P<load_duration>[\d\.ywduhmnsµμ]+)\s+'
                    'prompt eval count\:\s+?(?P<prompt_eval_count>\d+).+\s+'
                    'prompt eval duration\:\s+?(?P<prompt_eval_duration>[\d\.ywduhmnsµμ]+)\s+'
                    'prompt eval rate\:\s+?(?P<prompt_eval_rate>[\d\.]+).+\s+'
                    'eval count\:\s+?(?P<eval_count>\d+).+\s+'
                    'eval duration\:\s+?(?P<eval_duration>[\d\.ywduhmnsµμ]+)\s+'
                    'eval rate\:\s+?(?P<eval_rate>[\d\.]+).+\s*'
                    '.*?$',
            flags=re.MULTILINE | re.IGNORECASE | re.DOTALL,
        ),
        error_messages={
            'invalid': 'please copy & paste the whole text output after ollama execution'
        },
    )

    duplicate = fields.BooleanField(
        label='send me a copy of this report',
        initial=True,
    )

    def clean(self):
        cleaned_data = super(ReportSendForm, self).clean()
        for value in cleaned_data.values():
            if isinstance(value, str):
                try:
                    value.encode('ascii')
                except UnicodeEncodeError:
                    raise forms.ValidationError('Please use only English characters')
        return cleaned_data
