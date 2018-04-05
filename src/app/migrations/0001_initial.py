# Generated by Django 2.0.3 on 2018-03-13 08:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(max_length=256)),
                ('address', models.CharField(db_index=True, max_length=34)),
                ('uptime', models.FloatField(blank=True, null=True)),
                ('approval', models.FloatField(blank=True, null=True)),
                ('forged', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('proposal', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=256)),
                ('os', models.CharField(max_length=256)),
                ('cpu', models.CharField(max_length=256)),
                ('memory', models.CharField(max_length=256)),
                ('disk', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('timezone', models.CharField(max_length=256)),
                ('is_relay', models.BooleanField(default=False)),
                ('is_backup', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('delegate', models.ManyToManyField(related_name='nodes', to='app.Delegate')),
            ],
        ),
        migrations.CreateModel(
            name='VoteHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voters', models.IntegerField(blank=True, null=True)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('delegate', models.ManyToManyField(related_name='vote_history', to='app.Delegate')),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='delegate',
            field=models.ManyToManyField(related_name='contributions', to='app.Delegate'),
        ),
    ]
