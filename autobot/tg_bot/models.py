from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    tg_id = models.PositiveIntegerField(unique=True, verbose_name='Идентификатор пользователя в Telegram')
    tg_name = models.CharField(max_length=50, verbose_name='Имя пользователя в Telegram')

    def __str__(self, ):
        return f'{self.tg_id}_{self.tg_name}'

    class Meta:
        verbose_name = 'Телеграм Профиль'
        verbose_name_plural = 'Телеграм Профили'

class Automobile(models.Model):
    brand = models.CharField(max_length=90, verbose_name="Марка")
    a_model = models.CharField(max_length=115, verbose_name="Модель")
    reg_num = models.CharField(max_length=9, unique=True, verbose_name="Гос.Номер")

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self, ):
        return f'{self.brand} {self.a_model} ({self.reg_num})'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

class Refuilings(models.Model):
    REFUELING, MAINTENANCE, INSURANCE, TIRES, PARKING, TOLL_ROAD, FINE = map(chr, range(7,14))
    TYPES_CHOICES = [
        (REFUELING, 'Заправка'),
        (MAINTENANCE, 'ТО'),
        (INSURANCE, 'Страховка'),
        (TIRES, 'Шины/Шиномонтаж'),
        (PARKING, 'Парковка'),
        (TOLL_ROAD, 'Платная дорога'),
        (FINE, 'Штрафы'),
    ]

    car = models.ForeignKey(Automobile, on_delete=models.CASCADE, verbose_name="Автомобиль")
    ts = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    cost_type = models.CharField(max_length=3, choices=TYPES_CHOICES, default=REFUELING, verbose_name="Тип расхода")

    car_mileage = models.PositiveIntegerField(null=True, blank=True, verbose_name="Пробег")
    cost_summ = models.FloatField(verbose_name="Сумма расходов")
    liters = models.FloatField(null=True, blank=True, verbose_name="Литров")

    def __str__(self, ):
        return f'{self.car.reg_num} {self.car_mileage} {self.cost_type} {self.cost_summ}'

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
