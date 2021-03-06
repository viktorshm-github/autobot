# Generated by Django 3.2.6 on 2021-08-30 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.PositiveIntegerField(unique=True, verbose_name='Идентификатор пользователя в Telegram')),
                ('tg_name', models.CharField(max_length=50, verbose_name='Имя пользователя в Telegram')),
            ],
            options={
                'verbose_name': 'Телеграм Профиль',
                'verbose_name_plural': 'Телеграм Профили',
            },
        ),
        migrations.CreateModel(
            name='Automobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=90, verbose_name='Марка')),
                ('a_model', models.CharField(max_length=115, verbose_name='Модель')),
                ('reg_num', models.CharField(max_length=9, verbose_name='Гос.Номер')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg_bot.profile', verbose_name='Владелец')),
            ],
        ),
    ]
