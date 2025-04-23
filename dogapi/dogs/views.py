from django.db.models import Avg, Count, OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """
   ViewSet для работы с породами животных.

   Атрибуты:
    queryset (QuerySet): Запрос к базе данных, который возвращает все породы животных с аннотацией dogs_count,
    которая содержит количество собак каждой породы.
    serializer_class (Serializer): Класс сериализатора, который используется для преобразования данных породы
    в JSON и обратно.
   """
    queryset = Breed.objects.annotate(
        dogs_count=Count('dogs'))
    serializer_class = BreedSerializer


class DogViewSet(viewsets.ModelViewSet):
   """
   ViewSet для работы с собаками.

   Атрибуты:
   serializer_class (Serializer): Класс сериализатора, который используется для преобразования данных
   собаки в JSON и обратно.
   """
   serializer_class = DogSerializer

   def get_queryset(self):
       """
       Возвращает запрос к базе данных, который возвращает все собаки с аннотацией average_age,
       которая содержит средний возраст породы, к которой принадлежит собака.

       Если текущее действие является 'retrieve', то запрос также включает аннотацию same_breed_count,
       которая содержит количество собак той же породы.
       """
       # Подсчет среднего возраста порды к которой принадлежит собака
       avg_age_subquery = Breed.objects.filter(
           id=OuterRef('breed_id')
       ).annotate(
           avg_age=Avg('dogs__age')
       ).values('avg_age')[:1]

       queryset = Dog.objects.select_related('breed').annotate(
           average_age=Subquery(avg_age_subquery)
       )

       if self.action == 'retrieve':
           same_breed_count = Dog.objects.filter(
               breed_id=OuterRef('breed_id')
           ).values('breed_id').annotate(
               count=Count('id')
           ).values('count')[:1]

           queryset = queryset.annotate(
               same_breed_count=Subquery(same_breed_count)
           )

       return queryset

   def list(self, request, *args, **kwargs):
       """
       Возвращает список всех собак.
       """
       queryset = self.get_queryset()
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data)

   def retrieve(self, request, *args, **kwargs):
       """
       Возвращает данные одной собаки.
       """
       instance = self.get_object()
       serializer = self.get_serializer(instance)
       return Response(serializer.data)

