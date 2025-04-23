from rest_framework.serializers import ModelSerializer, IntegerField, CharField, FloatField
from .models import Dog, Breed


class BreedSerializer(ModelSerializer):
    dogs_count = IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = [
            'id', 'name', 'size', 'friendliness',
            'trainability', 'shedding_amount', 'exercise_needs', 'dogs_count'
        ]


class DogSerializer(ModelSerializer):
    breed_name = CharField(source='breed.name', read_only=True)
    average_age = FloatField(read_only=True)
    same_breed_count = IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = [
            'id', 'name', 'age', 'breed', 'breed_name', 'gender',
            'color', 'favorite_food', 'favorite_toy',
            'average_age', 'same_breed_count'
        ]