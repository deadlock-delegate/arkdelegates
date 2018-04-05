# Generated by Django 2.0.3 on 2018-03-27 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_node_has_arkstats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contribution',
            name='delegate',
        ),
        migrations.AddField(
            model_name='contribution',
            name='delegate',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='app.Delegate'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='node',
            name='delegate',
        ),
        migrations.AddField(
            model_name='node',
            name='delegate',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='app.Delegate'),
            preserve_default=False,
        ),
    ]
