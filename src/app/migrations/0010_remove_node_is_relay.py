# Generated by Django 2.0.3 on 2018-03-30 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_node_network'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='is_relay',
        ),
    ]
