from django.shortcuts import render
from places.models import Place
from django.http import HttpResponse, HttpRequest
from django.templatetags.static import static

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
                        "detailsUrl": static("places/moscow_legends.json") 
                        if place.title == "Экскурсионная компания «Легенды Москвы»"
                        else static("places/roofs24.json")
                    }
                }

        features.append(feature)

    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    print(places_geojson)
    return render(request, 'index.html', {'places_geojson': places_geojson})