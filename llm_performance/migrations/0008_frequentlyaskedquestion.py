# Generated by Django 3.2.19 on 2024-01-20 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_performance', '0007_rename_llm_model_sampleinput_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequentlyAskedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, default=None, null=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
    ]
