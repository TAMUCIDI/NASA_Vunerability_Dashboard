# Generated by Django 3.2.18 on 2023-04-14 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_auto_20230413_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='maps',
            name='ProtectedAreaDistWeight',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
