# Generated by Django 2.1.7 on 2019-03-01 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20190214_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reference_number',
            field=models.CharField(default='', max_length=32),
        ),
    ]