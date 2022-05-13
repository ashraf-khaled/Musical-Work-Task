from django.contrib import admin

from .models import MusicalWorkMetaDataFile, MusicalWork


@admin.register(MusicalWorkMetaDataFile)
class MusicalWorkMetaDataFileAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "file",
        "is_processed",
    ]


@admin.register(MusicalWork)
class MusicalWorkAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "title",
        "contributors",
        "iswc",
    ]
