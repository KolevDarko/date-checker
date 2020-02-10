# Generated by Django 3.0.2 on 2020-02-10 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200126_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=7)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='api.Product')),
            ],
        ),
    ]