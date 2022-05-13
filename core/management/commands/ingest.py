import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models import MusicalWorkMetaDataFile, MusicalWork


def process_file(file):
    data = pd.read_csv(file)
    for index, row in data.iterrows():
        iswc = row("iswc")
        title = row("title")
        contributors = row("contributors", "").split("|")
        work = None
        if iswc is not None:
            work = MusicalWork.objects.filter(iswc=iswc).first()
            if work is None:
                qs = Q()
                for con in contributors:
                    qs |= Q(contributors__icontains=con)
                work = MusicalWork.objects.filter(Q(title=title), qs).first()
            if work is None:
                MusicalWork.objects.create(
                    title=title,
                    iswc=iswc,
                    contributors="|".join(contributors),
                )
            else:
                work.iswc = work.iswc or iswc
                work.contributors = "|".join(
                    set(work.contributors.split("|") + contributors)
                )
                work.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(f"Processing input files for reconciliation.")
        )
        work_files = MusicalWorkMetaDataFile.objects.all()
        if not work_files:
            self.stdout.write(self.style.ERROR(f"No files were found."))

        for work_file in work_files:
            filename = f"#{work_file.pk}-{work_file.file.name}"

            self.stdout.write(self.style.WARNING(f"Parsing: {filename}."))

            if work_file.is_processed:
                self.stdout.write(
                    self.style.WARNING(
                        f"File: {filename} is marked as processed and will be skipped."
                    )
                )

            try:
                process_file(work_file.file)
            except Exception as ex:
                self.stdout.write(
                    self.style.ERROR(f"Error while parsing {filename}: {ex}.")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Parsing: {filename} completed successfully.")
                )
                work_file.is_processed = True
                work_file.save()
