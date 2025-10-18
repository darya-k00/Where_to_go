import requests
import logging
import os

from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from pydantic import BaseModel, ValidationError, field_validator, Field
from typing import List
from requests.exceptions import JSONDecodeError, HTTPError
from decimal import Decimal
from urllib.parse import urlparse

from places.models import Image, Place

logger = logging.getLogger(__name__)


class CoordinatesSchema(BaseModel):
    lng: float
    lat: float

    @field_validator("lng", "lat")
    @classmethod
    def validate_coordinates(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("Значение должны находится в диапазоне от -180 до 180")
        return round(v, 17)


class PlaceSchema(BaseModel):
    title: str
    imgs: List[str]
    short_description: str = Field(alias="description_short")
    long_description: str = Field(alias="description_long")
    coordinates: CoordinatesSchema


class Command(BaseCommand):
    help = "Загрузка мест из json-файла"

    def add_arguments(self, parser) -> None:
        parser.add_argument("url", type=str, help="URL json с данными места")

    def handle(self, *args, **options) -> None:
        url = options["url"]
        try:
            response = requests.get(url)
            response.raise_for_status()

            validated_data = PlaceSchema(**response.json())
            try:
                place, created = Place.objects.get_or_create(
                    title=validated_data.title,
                    lat=Decimal(str(validated_data.coordinates.lat)),
                    lng=Decimal(str(validated_data.coordinates.lng)),
                    defaults={
                        "short_description": validated_data.short_description,
                        "long_description": validated_data.long_description,
                    }
                )
            except MultipleObjectsReturned:
                logger.error("Найдено несколько мест")
                return

            self.update_images(place, validated_data.imgs)
            logger.info(
                f"Место '{place.title}' успешно {'создано' if created else 'обновлено'}"
            )

        except HTTPError:
            logger.error("Ошибка запроса")
        except JSONDecodeError:
            logger.error("Ошибка на стороне сервера: невалидный json")
        except ValidationError as val:
            logger.error(f"Ошибка валидации данных: {val.errors()}")
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")

    def update_images(self, place: Place, image_urls: List[str]) -> None:
        place.images.all().delete()

        for position, url in enumerate(image_urls, start=1):
            try:
                img_response = requests.get(url)
                img_response.raise_for_status()

                image_name = os.path.basename(urlparse(url).path)
                image_file = ContentFile(img_response.content, name=image_name)

                Image.objects.create(
                    place=place,
                    image=image_file,
                    number=position
                )
            except Exception as e:
                logger.error(f"Не удалось загрузить изображение {url}: {e}")