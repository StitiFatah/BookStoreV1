# Generated by Django 3.0.7 on 2020-07-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20200709_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='auto_complete',
            field=models.BooleanField(default=False),
        ),
    ]
