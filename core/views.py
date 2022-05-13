from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, generics
from .models import MusicalWork
from .serializers import MusicalWorkMetaDataFileSerializer, MusicalWorkSerializer


class MusicAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    queryset = MusicalWork.objects.none()

    def get_serializer_class(self):
        """Return the serializer class given the action"""
        action = self.action
        if self.action == "create" or self.action == "list":
            return MusicalWorkMetaDataFileSerializer
        else:
            return MusicalWorkSerializer

    def get(self, request: Request, *args, **kwargs):
        iswc = request.query_params.get("iswc")
        if iswc is not None:
            work = MusicalWork.objects.filter(iswc=iswc).first()
            if work is not None:
                serializer = MusicalWorkSerializer(work)
                queryset = serializer.data
        return super().list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        works_file = serializer.save()
        return Response(data={"file": works_file.file.name})
