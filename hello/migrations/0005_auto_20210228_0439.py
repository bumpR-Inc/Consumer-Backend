# Generated by Django 2.1.4 on 2021-02-28 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_addin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addin',
            name='menuItems',
            field=models.ManyToManyField(null=True, related_name='add_ins', to='hello.MenuItem'),
        ),
        migrations.AlterField(
            model_name='addin',
            name='orderItems',
            field=models.ManyToManyField(null=True, related_name='add_ins', to='hello.OrderItem'),
        ),
    ]
