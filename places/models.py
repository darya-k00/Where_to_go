from django.db import models

class Place(models.Model):
    title = models.CharField(verbose_name="Название", max_length=80, blank=True)
    description_short = models.TextField(verbose_name="Краткое описание", max_length=300, blank=True)
    description_long = models.TextField(verbose_name="Описание", blank=True)
    lng = models.DecimalField(verbose_name='Долгота', max_digits=20, decimal_places=17)
    lat = models.DecimalField(verbose_name='Шировата', max_digits=20, decimal_places=17)

    def __str__(self) -> str:
        return self.title