# Generated by Django 4.2.6 on 2023-11-01 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkelement',
            name='level',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2')], max_length=50),
        ),
    ]
