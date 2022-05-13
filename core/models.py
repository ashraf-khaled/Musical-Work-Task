from django.db import models


class MusicalWorkMetaDataFile(models.Model):
    file = models.FileField()
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"MusicalWorkMetaDataFile: #{self.pk}"


class MusicalWork(models.Model):
    title = models.CharField(max_length=255)
    contributors = models.TextField()
    iswc = models.CharField(max_length=16, unique=True, blank=True, null=True)

    @property
    def contributors_list(self):
        return self.contributors.split("|") if self.contributors is not None else []

    def __str__(self):
        return f"MusicalWork: #{self.pk}"
