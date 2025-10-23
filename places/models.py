from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(verbose_name="Название", max_length=80)
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    long_description = HTMLField(verbose_name="Описание", blank=True)
    lng = models.DecimalField(verbose_name="Долгота", max_digits=20, decimal_places=17)
    lat = models.DecimalField(verbose_name="Широта", max_digits=20, decimal_places=17)

    class Meta:
        verbose_name = 'Место',
        verbose_name_plural = 'Места'
        ordering = ['title']
        unique_together = [('title', 'lng', 'lat')]

    def __str__(self) -> str:
        return self.title

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="Место на карте", related_name="images")
    image = models.ImageField(verbose_name="Картинка", upload_to="")
    number = models.PositiveIntegerField(verbose_name="Позиция", default=1, db_index=True)

  class Meta:
      verbose_name = 'Картинка'
   	  verbose_name_plural = 'Фотографии'
      ordering = ['number']


    def __str__(self):
        return f"{self.number} - {self.place.title}"
