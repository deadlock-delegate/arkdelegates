# Generated by Django 2.0.3 on 2018-04-01 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20180401_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='voting_power',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
