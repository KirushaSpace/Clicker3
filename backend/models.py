from django.db import models
from django.contrib.auth.models import User
from copy import copy
from .constants import *


class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=1)  # От уровня зависит количество бустов

    hp = models.IntegerField(default=10)
    hp_boss = models.IntegerField(default=10)
    damage = models.IntegerField(default=10)
    level_enemy = models.IntegerField(default=1)

    # Метод для установки текущего количества монет пользователя.
    def set_coins(self, coins, commit=True):
        self.coins = coins  # Теперь мы просто присваиваем входящее значение монет.
        is_levelupdated = self.is_levelup()  # Проверка на повышение уровня.
        boost_type = self.get_boost_type()  # Получение типа буста, который будет создан при повышении уровня.

        if is_levelupdated:
            self.level += 1
        if commit:
            self.save()

        return is_levelupdated, boost_type

    def set_hp(self, damage, commit=True):
        self.damage = damage
        is_next_hp = self.is_next_hp()
        if is_next_hp:
            self.level_enemy += 1
            self.hp = self.calculate_next_hp_enemy()
            self.damage = self.hp
        if commit:
            self.save()
        if self.level_enemy % 10 == 0:
            self.hp_boss = self.calculate_next_hp_boss()
            self.save()
            return self.hp_boss
        return self.hp

    # Выделили проверку на повышение уровня в отдельный метод для чистоты кода.
    def is_levelup(self):
        return self.coins >= self.calculate_next_level_price()

    # Выделили получение типа буста в отдельный метод для удобства.
    def get_boost_type(self):
        boost_type = 0
        if self.level % 3 == 0:
            boost_type = 1
        return boost_type

    # Поменяли название с check_level_price, потому что теперь так гораздо больше подходит по смыслу.
    def calculate_next_level_price(self):
        return (self.level ** 2) * 30 * self.level


    def calculate_next_hp_boss(self):
        return int(self.hp * 5)


    def is_next_hp(self):
        return self.damage <= 0


    def calculate_next_hp_enemy(self):
        return int(self.hp + self.hp // 4)


class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    def levelup(self, current_coins):
        if self.price > current_coins:  # Если монет недостаточно, ничего не делаем.
            return False

        self.core.coins = current_coins - self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale'] # Умножаем силу клика на константу.
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale'] # Умножаем силу автоклика на константу.
        self.core.save()

        old_boost_stats = copy(self)

        self.level += 1
        if self.level % 10 == 0:
            self.power = int(self.power * 2)
        self.price = int(self.price * 0.6 * BOOST_TYPE_VALUES[self.type]['price_scale']) # Умножаем ценник на константу.
        self.save()

        return old_boost_stats, self
