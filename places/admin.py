from django.contrib import admin
from places.models import Place, Image


@admin.register(Place)
class AdminPlace(admin.ModelAdmin):
    list_display = ("title", )
    fieldsets = (
        (None, {
            "fields": ("title", "description_short",
                       "description_long", "lng", "lat"),
        }),
    )

@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    raw_id_fields = ["place"]