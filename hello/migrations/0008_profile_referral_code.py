# Generated by Django 2.1.4 on 2021-03-05 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_merge_20210228_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
