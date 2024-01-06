# Generated by Django 3.2.19 on 2024-01-06 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('input', models.TextField()),
                ('cpu', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('cpu_brand', models.CharField(blank=True, db_index=True, default=None, max_length=16, null=True)),
                ('ram', models.IntegerField(blank=True, db_index=True, default=None, null=True)),
                ('gpu', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('gpu_brand', models.CharField(blank=True, db_index=True, default=None, max_length=16, null=True)),
                ('vram', models.IntegerField(blank=True, db_index=True, default=None, null=True)),
                ('total_duration', models.FloatField()),
                ('load_duration', models.FloatField()),
                ('prompt_eval_count', models.IntegerField()),
                ('prompt_eval_duration', models.FloatField()),
                ('prompt_eval_rate', models.FloatField()),
                ('eval_count', models.IntegerField()),
                ('eval_duration', models.FloatField()),
                ('eval_rate', models.FloatField()),
                ('llm_model', models.CharField(blank=True, db_index=True, default=None, max_length=16, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
