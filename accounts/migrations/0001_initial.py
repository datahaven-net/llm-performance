# Generated by Django 3.2.19 on 2023-12-31 13:07

from django.conf import settings
import django.contrib.auth.models
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(help_text='user email address', max_length=255, unique=True, verbose_name='email address')),
                ('notes', models.TextField(blank=True, default=None, help_text='any note regarding this account', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'base_manager_name': 'users',
                'default_manager_name': 'users',
            },
            managers=[
                ('users', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('started', 'STARTED'), ('sent', 'SENT'), ('failed', 'FAILED')], default='started', max_length=10)),
                ('type', models.CharField(choices=[('email', 'EMAIL'), ('sms', 'SMS')], default='email', max_length=10)),
                ('subject', models.CharField(choices=[('some_subject', 'SOME SUBJECT')], max_length=32)),
                ('details', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'base_manager_name': 'notifications',
                'default_manager_name': 'notifications',
            },
            managers=[
                ('notifications', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
