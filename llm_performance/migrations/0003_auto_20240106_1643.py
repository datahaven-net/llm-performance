# Generated by Django 3.2.19 on 2024-01-06 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('llm_performance', '0002_auto_20240106_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='performancesnapshot',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='performancesnapshot',
            name='cpu_brand',
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='performancesnapshot',
            name='gpu_brand',
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='performancesnapshot',
            name='reporter',
            field=models.ForeignKey(default='admin@admin.admin', on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='accounts.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='performancesnapshot',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
