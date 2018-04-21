from rest_framework import generics
from .serializer import AuthorModelSerializer, CreationModelSerializer

from main_app.models import Author, Creation


class AuthorListAPIView(generics.ListAPIView):
    serializer_class = AuthorModelSerializer

    def get_queryset(self):
        return Author.objects.all()