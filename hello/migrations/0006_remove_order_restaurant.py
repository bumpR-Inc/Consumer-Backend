# Generated by Django 2.1.4 on 2021-02-02 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20210128_0324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
    ]
