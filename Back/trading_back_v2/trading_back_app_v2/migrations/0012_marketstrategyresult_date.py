# Generated by Django 5.1.1 on 2024-10-23 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_back_app_v2', '0011_marketstrategyresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketstrategyresult',
            name='date',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
