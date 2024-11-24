# Generated by Django 5.1.1 on 2024-09-23 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_back_app_v2', '0003_delete_backtest_delete_indicatorbollingerband_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('strategyName', models.CharField(max_length=100)),
                ('tradesCount', models.FloatField()),
                ('worstDrawback', models.FloatField()),
                ('averagePositifTrade', models.FloatField()),
                ('averageNegativeTrade', models.FloatField()),
                ('strategyParameter', models.TextField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorBollingerBand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('BB_Lower', models.FloatField()),
                ('BB_Middle', models.FloatField()),
                ('BB_Upper', models.FloatField()),
                ('BB_Bandwidth', models.FloatField()),
                ('BB_Percent', models.FloatField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorEMA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('close_price', models.FloatField()),
                ('EMA20', models.FloatField()),
                ('EMA50', models.FloatField(blank=True, null=True)),
                ('EMA200', models.FloatField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorIchimoku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('Ichimoku_Conversion', models.FloatField()),
                ('Ichimoku_Base', models.FloatField()),
                ('Ichimoku_LeadingA', models.FloatField()),
                ('Ichimoku_LeadingB', models.FloatField()),
                ('Ichimoku_Lagging', models.FloatField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorMACD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('macd', models.FloatField()),
                ('macd_signal', models.FloatField()),
                ('macd_histogram', models.FloatField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorRSI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('rsi_7', models.FloatField()),
                ('rsi_14', models.FloatField()),
                ('rsi_21', models.FloatField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorSMA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('close_price', models.FloatField()),
                ('MM10', models.FloatField()),
                ('MM15', models.FloatField(blank=True, null=True)),
                ('MM20', models.FloatField(blank=True, null=True)),
                ('MM25', models.FloatField(blank=True, null=True)),
                ('MM30', models.FloatField(blank=True, null=True)),
                ('MM35', models.FloatField(blank=True, null=True)),
                ('MM40', models.FloatField(blank=True, null=True)),
                ('MM45', models.FloatField(blank=True, null=True)),
                ('MM50', models.FloatField(blank=True, null=True)),
                ('MM55', models.FloatField(blank=True, null=True)),
                ('MM60', models.FloatField(blank=True, null=True)),
                ('MM65', models.FloatField(blank=True, null=True)),
                ('MM70', models.FloatField(blank=True, null=True)),
                ('MM75', models.FloatField(blank=True, null=True)),
                ('MM80', models.FloatField(blank=True, null=True)),
                ('MM85', models.FloatField(blank=True, null=True)),
                ('MM90', models.FloatField(blank=True, null=True)),
                ('MM95', models.FloatField(blank=True, null=True)),
                ('MM100', models.FloatField(blank=True, null=True)),
                ('MM200', models.FloatField(blank=True, null=True)),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='IndicatorStochastic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('stochastic_k', models.FloatField()),
                ('stochastic_d', models.FloatField()),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='StrategyDataTendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('close_price', models.FloatField()),
                ('pente_SMMA20', models.FloatField()),
                ('pente_SMMA50', models.FloatField()),
                ('pente_SMMA200', models.FloatField()),
                ('tendance_SMMA20', models.CharField(max_length=50)),
                ('tendance_SMMA50', models.CharField(max_length=50)),
                ('tendance_SMMA200', models.CharField(max_length=50)),
                ('tendance_all', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date')},
            },
        ),
        migrations.CreateModel(
            name='TradingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
                ('interval_time', models.CharField(max_length=10)),
                ('date_start', models.CharField(max_length=50)),
                ('date_end', models.CharField(max_length=50)),
                ('strategyName', models.CharField(max_length=100)),
                ('strategyParameter', models.TextField()),
                ('buy_price', models.CharField(max_length=100)),
                ('sell_price', models.CharField(max_length=100)),
                ('dollars_profit', models.CharField(max_length=100)),
                ('percent_profit', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('market', 'interval_time', 'date_start')},
            },
        ),
    ]