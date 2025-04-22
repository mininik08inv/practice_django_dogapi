from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Breed(models.Model):
    # Класс модели представляющий породй собак
    SIZE_CHOICES = [
        ('Tiny', 'Tiny'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    name = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    friendliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    trainability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    shedding_amount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    exercise_needs = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"


    def get_absolute_url(self):
        return reverse('breeds', kwargs={'breed_id': self.pk})


class Dog(models.Model):
    # Класс модели представляющий конретную собаку
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1)])
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name='dogs'
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    color = models.CharField(max_length=50)
    favorite_food = models.CharField(max_length=100, null=True, blank=True, default='Не известна')
    favorite_toy = models.CharField(max_length=100, null=True, blank=True, default='Не известна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"


    def get_absolute_url(self):
        return reverse('dogs', kwargs={'dog_id': self.pk})
