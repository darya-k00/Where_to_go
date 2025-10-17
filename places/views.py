from django.shortcuts import render
from places.models import Place
from django.http import HttpResponse, HttpRequest
from django.templatetags.static import static
from django.shortcuts import get_object_or_404

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
    return render(request, "index.html", {"places_geojson": places_geojson})


def view_place(request: HttpRequest, pk: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=pk)

    return render(request, "place.html", context={"place": place})