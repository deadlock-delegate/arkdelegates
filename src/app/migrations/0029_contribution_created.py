# Generated by Django 2.1.7 on 2019-03-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20180603_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
