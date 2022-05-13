from rest_framework import serializers

from .models import MusicalWorkMetaDataFile, MusicalWork


class MusicalWorkMetaDataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicalWorkMetaDataFile
        fields = ["file"]


class MusicalWorkSerializer(serializers.ModelSerializer):
    contributors = serializers.ListField(source="contributors_list")

    class Meta:
        model = MusicalWork
        fields = [
            "iswc",
            "title",
            "contributors",
        ]
