import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from pydantic import BaseModel, ValidationError, field_validator
from typing import List
from requests.exceptions import JSONDecodeError, HTTPError

from places.models import Image, Place


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
    description_short: str
    description_long: str
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
            raw_place = response.json()

            place_data = PlaceSchema(**raw_place)

            place, created = Place.objects.get_or_create(
                title=place_data.title,
                defaults={
                    "description_short": place_data.description_short,
                    "description_long": place_data.description_long,
                    "lng": place_data.coordinates.lng,
                    "lat": place_data.coordinates.lat,
                }
            )

            self.update_images(place, place_data.imgs)

            self.stdout.write(
                f"Место '{place.title}' успешно {'создано' if created else 'обновлено'}"
            )

        except HTTPError:
            self.stdout.write("Ошибка запроса")
        except JSONDecodeError:
            self.stdout.write("Ошибка на стороне сервера: невалидный json")
        except ValidationError as val:
            self.stdout.write(f"Ошибка валидации данных: {val.errors()}")
        except Exception as e:
            self.stdout.write(f"Ошибка: {str(e)}")

    def update_images(self, place: Place, image_urls: List[str]) -> None:
        place.images.all().delete()

        for position, url in enumerate(image_urls, start=1):
            try:
                img_response = requests.get(url)
                img_response.raise_for_status()

                image_name = url.split("/")[-1]
                image_file = ContentFile(img_response.content, name=image_name)

                Image.objects.create(
                    place=place,
                    image=image_file,
                    number=position
                )
            except Exception as e:
                self.stdout.write(f"Не удалось загрузить изображение {url}: {e}")