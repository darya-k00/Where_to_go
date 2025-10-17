from django.db import models

class Place(models.Model):
    title = models.CharField(verbose_name="Название", max_length=80, blank=True)
    description_short = models.TextField(verbose_name="Краткое описание", max_length=300, blank=True)
    description_long = models.TextField(verbose_name="Описание", blank=True)
    lng = models.DecimalField(verbose_name="Долгота", max_digits=20, decimal_places=17)
    lat = models.DecimalField(verbose_name="Шировата", max_digits=20, decimal_places=17)

    def __str__(self) -> str:
        return self.title

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="Место на карте", related_name="images")
    image = models.ImageField(verbose_name="Картинка", upload_to="media/", blank=True)
    number = models.PositiveIntegerField(verbose_name="Номер", default=1, db_index=True)

    def __str__(self):
        return f"#{self.number} - {self.place.title}"