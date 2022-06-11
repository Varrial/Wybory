from django.contrib.auth.models import User
from django.db import models

# TYP = (
#     ('prezydenckie', 'Prezydenckie'),
#     ('parlamentarne', 'Parlamentarne'),
#     ('starosty', 'Starosty roku'),
#     ('dziekana', 'Dziekana wydziału'),
# )

# class Osoba(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     data_urodzenia = models.DateField()
#     miejsce_zameldowania = models.TextField()
#     class Meta:
#         verbose_name_plural = 'Osoby'
from django.utils import timezone


class TypWyborow(models.Model):
    typ = models.CharField(max_length=40, unique=True)
    class Meta:
        verbose_name_plural = 'Typy Wyborów'

    def __str__(self):
        return self.typ.__str__()


class Wybory(models.Model):
    nazwa = models.CharField(max_length=255)
    typ = models.ForeignKey(TypWyborow, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField(default=timezone.now)
    data_zakonczenia = models.DateTimeField(default=timezone.now)
    czy_aktywne = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Wybory'
    def __str__(self):
        return self.nazwa

class Uprawnieni(models.Model):
    id_wyborow = models.ForeignKey(Wybory, on_delete=models.CASCADE)
    pesel = models.ForeignKey(User, on_delete=models.CASCADE)
    CzyZaglosowal = models.BooleanField(default=False, verbose_name = "Czy Zagłosował?")
    class Meta:
        verbose_name_plural = 'Uprawnieni'

class Kandydaci(models.Model):
    id_wyborow = models.ForeignKey(Wybory, on_delete=models.CASCADE)
    pesel = models.ForeignKey(User, on_delete=models.CASCADE)
    poparcie = models.PositiveSmallIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Kandydaci'
    def __str__(self):
        return self.pesel.__str__()
