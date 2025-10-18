from adminsortable2.admin import SortableAdminMixin, SortableStackedInline
from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html

class ImageInline(SortableStackedInline):
    model = Image
    extra = 0
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width:200px; max-height:200px;" />')
    get_preview.short_description = "Preview"

@admin.register(Place)
class AdminPlace(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", )
    fieldsets = (
        (None, {
            "fields": ("title", "description_short",
                       "description_long", "lng", "lat"),
        }),
    )
    inlines = [ImageInline]

@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    raw_id_fields = ["place"]