# Generated by Django 2.0.5 on 2018-06-03 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_history_delegate_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='delegate_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='app.Delegate'),
        ),
    ]
