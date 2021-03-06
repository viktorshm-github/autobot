# Generated by Django 3.2.6 on 2021-08-31 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='automobile',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterField(
            model_name='automobile',
            name='reg_num',
            field=models.CharField(max_length=9, unique=True, verbose_name='Гос.Номер'),
        ),
        migrations.CreateModel(
            name='Refuilings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('cost_type', models.CharField(choices=[('\x07', 'Заправка'), ('\x08', 'ТО'), ('\t', 'Страховка'), ('\n', 'Шины/Шиномонтаж'), ('\x0b', 'Парковка'), ('\x0c', 'Платная дорога'), ('\r', 'Штрафы')], default='\x07', max_length=3, verbose_name='Тип расхода')),
                ('car_mileage', models.PositiveIntegerField(blank=True, null=True, verbose_name='Пробег')),
                ('cost_summ', models.FloatField(verbose_name='Сумма расходов')),
                ('liters', models.FloatField(blank=True, null=True, verbose_name='Литров')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg_bot.automobile', verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
            },
        ),
    ]
