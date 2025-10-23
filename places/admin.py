from adminsortable2.admin import SortableAdminMixin, SortableStackedInline
from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html


class ImageInline(SortableStackedInline):
    model = Image
    extra = 0
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px;" />', obj.image.url)
    get_preview.short_description = "Preview"


@admin.register(Place)
class AdminPlace(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", )
    fieldsets = (
        (None, {
            "fields": ("title", "short_description",
                       "long_description", "lng", "lat"),
        }),
    )
    inlines = [ImageInline]
    search_fields = ['title']


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    raw_id_fields = ["place"]
