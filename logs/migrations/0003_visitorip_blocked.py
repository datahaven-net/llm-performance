# Generated by Django 3.2.19 on 2024-01-30 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_visitorip'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorip',
            name='blocked',
            field=models.BooleanField(default=False, help_text='Requests are blocked'),
        ),
    ]