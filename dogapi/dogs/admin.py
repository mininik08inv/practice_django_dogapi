from django.contrib import admin
from .models import Dog, Breed


# Register your models here.

# Регистрируем модели для работы через админ-панель
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed')
    list_display_links = ('name', )
    list_per_page = 10
    search_fields = ['name__icontains']
    list_filter = ()


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'size',)
    list_display_links = ('name', )
    list_per_page = 10
    search_fields = ['name__icontains']
    list_filter = ()
