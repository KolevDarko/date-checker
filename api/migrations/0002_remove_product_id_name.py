# Generated by Django 3.0.2 on 2020-01-17 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id_name',
        ),
    ]