from rest_framework import serializers

from main_app.models import Author, Creation


class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'first_name',
            'last_name',
            'image',
            'profession',
            'graduated_school',
            'about',
            'rank'
        ]


class CreationModelSerializer(serializers.ModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Creation
        fields = [
            'author',
            'title',
            'co_authors',
            'type',
            'category',
            'subclass',
            'overview',
            'keyword',
            'created_date',
            'language',
            'price',
            'num_of_page',
            'uploaded_date',
            'total_downloads',
        ]
