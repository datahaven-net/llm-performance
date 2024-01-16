# -*- coding: UTF-8 -*-

import re

from django.forms import forms, fields, widgets


class ReportSendForm(forms.Form):

    name = fields.CharField(
        label='user name:',
        disabled=True,
        required=True,
    )

    email = fields.CharField(
        label='e-mail:',
        disabled=True,
        required=True,
    )

    cpu = fields.CharField(
        label='CPU model name:',
        help_text='enter full model name of your Central Processor Unit',
        max_length=256,
        required=True,
    )

    cpu_cores = fields.IntegerField(
        label='number of cores (optional):',
        help_text='enter number of cores in your CPU',
        min_value=1,
        max_value=256,
        required=False,
    )

    ram = fields.IntegerField(
        label='RAM size in Gigabytes (optional):',
        help_text='physical Random Access Memory size of your machine',
        min_value=1,
        required=False,
    )

    gpu = fields.CharField(
        label='GPU model name:',
        help_text='details about your Graphics Processing Unit model',
        max_length=256,
        required=True,
    )

    vram = fields.IntegerField(
        label='VRAM size in Gigabytes (optional):',
        help_text='Video Random Access Memory (GPU memory) size',
        min_value=1,
        required=False,
    )

    purchase_year = fields.IntegerField(
        label='year the system was purchased (optional):',
        help_text='you can disclose here when you bought your computer',
        min_value=1980,
        max_value=2024,
        required=False,
    )

    purchase_price = fields.IntegerField(
        label='approximate price in U.S. $ (optional):',
        help_text='you can also indicate the approximate price at the time of purchase',
        min_value=1,
        max_value=100000,
        required=False,
    )

    operating_system = fields.CharField(
        label='operating system (optional):',
        help_text='description of your operation system',
        max_length=256,
        required=False,
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
        max_length=1024*50,
        regex=re.compile(
            pattern='^.*?ollama\s+run\s+.*?(?P<llm_model>[\w\:\-\_\.]+)\s+.*?'
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
            'invalid': 'Please copy & paste the whole text output after ollama execution, run ollama with "--verbose" flag.'
        },
        required=True,
    )

    def clean(self):
        cleaned_data = super(ReportSendForm, self).clean()
        for name, value in cleaned_data.items():
            if name != 'message':
                if isinstance(value, str):
                    try:
                        value.encode('ascii')
                    except UnicodeEncodeError:
                        raise forms.ValidationError('Please use only English characters.')
        return cleaned_data
