# Generated by Django 2.1.4 on 2020-10-04 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_auto_20200912_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preferences_of_user', to='hello.Profile'),
        ),
    ]
