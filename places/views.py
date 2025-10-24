from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from places.models import Place

def view_index(request: HttpRequest) -> HttpResponse:
    places = Place.objects.all()

    features = []
    for place in places:
        feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.lng, place.lat]
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": reverse(view_places, args=[place.id]) 
                    }
                }

        features.append(feature)

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return render(request, "index.html", {"places_geojson": places_geojson})


def view_places(request: HttpRequest, pk: int) -> HttpResponse:
    place = get_object_or_404(Place.objects.prefetch_related('images'),pk=pk)
    images = place.images.all()

    serialize_data = {
        "title": place.title,
        "imgs":[img.image.url for img in images],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }

    return JsonResponse(serialize_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})
