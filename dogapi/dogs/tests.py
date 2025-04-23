from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Dog, Breed


class DogBreedAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестовые породы
        self.breed1 = Breed.objects.create(
            name="Дворняжка",
            size="Large",
            friendliness=5,
            trainability=4,
            shedding_amount=3,
            exercise_needs=4
        )
        self.breed2 = Breed.objects.create(
            name="Чихуахуа",
            size="Small",
            friendliness=3,
            trainability=3,
            shedding_amount=2,
            exercise_needs=2
        )

        # Создаем тестовых собак
        self.dog1 = Dog.objects.create(
            name="Рекс",
            age=3,
            breed=self.breed1,
            gender="Male",
            color="Black",
            favorite_food="Meat",
            favorite_toy="Ball"
        )
        self.dog2 = Dog.objects.create(
            name="Машка",
            age=5,
            breed=self.breed1,
            gender="Female",
            color="Brown",
            favorite_food="Fish",
            favorite_toy="Bone"
        )
        self.dog3 = Dog.objects.create(
            name="Бобик",
            age=2,
            breed=self.breed2,
            gender="Male",
            color="White",
            favorite_food="Chips",
            favorite_toy="Rope"
        )

    # DOG TESTS

    def test_get_dogs_list(self):
        """Тест GET /api/dogs/ - должен включать средний возраст по породам"""
        url = reverse('dog-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Проверяем что есть поле average_age
        for dog in response.data:
            self.assertIn('average_age', dog)

        # Проверяем расчет среднего возраста для породы
        labrador_dogs = [d for d in response.data if d['breed'] == self.breed1.id]
        self.assertEqual(len(labrador_dogs), 2)
        self.assertEqual(labrador_dogs[0]['average_age'], 4.0)  # (3+5)/2=4

    def test_create_dog(self):
        """Тест POST /api/dogs/"""
        url = reverse('dog-list')
        data = {
            "name": "New Dog",
            "age": 4,
            "breed": self.breed1.id,
            "gender": "Male",
            "color": "Red",
            "favorite_food": "Beef",
            "favorite_toy": "Frisbee"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.count(), 4)
        self.assertEqual(Dog.objects.get(id=response.data['id']).name, "New Dog")

    def test_get_single_dog(self):
        """Тест GET /api/dogs/<id> - должен включать количество собак той же породы"""
        url = reverse('dog-detail', args=[self.dog1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('same_breed_count', response.data)
        self.assertEqual(response.data['same_breed_count'], 2)  # 2 лабрадора

    def test_update_dog(self):
        """Тест PUT /api/dogs/<id>"""
        url = reverse('dog-detail', args=[self.dog1.id])
        data = {
            "name": "Rex Updated",
            "age": 4,
            "breed": self.breed1.id,
            "gender": "Male",
            "color": "Black",
            "favorite_food": "Meat",
            "favorite_toy": "Ball"
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dog1.refresh_from_db()
        self.assertEqual(self.dog1.name, "Rex Updated")

    def test_delete_dog(self):
        """Тест DELETE /api/dogs/<id>"""
        url = reverse('dog-detail', args=[self.dog1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 2)
        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(id=self.dog1.id)

    # BREED TESTS

    def test_get_breeds_list(self):
        """Тест GET /api/breeds/ - должен включать количество собак каждой породы"""
        url = reverse('breed-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Проверяем что есть поле dogs_count
        for breed in response.data:
            self.assertIn('dogs_count', breed)

        # Проверяем подсчет собак
        labrador = next(b for b in response.data if b['id'] == self.breed1.id)
        self.assertEqual(labrador['dogs_count'], 2)

        chihuahua = next(b for b in response.data if b['id'] == self.breed2.id)
        self.assertEqual(chihuahua['dogs_count'], 1)

    def test_create_breed(self):
        """Тест POST /api/breeds/"""
        url = reverse('breed-list')
        data = {
            "name": "Овчарка немецкая",
            "size": "Medium",
            "friendliness": 4,
            "trainability": 5,
            "shedding_amount": 2,
            "exercise_needs": 3
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.count(), 3)
        self.assertEqual(Breed.objects.get(id=response.data['id']).name, "Овчарка немецкая")

    def test_get_single_breed(self):
        """Тест GET /api/breeds/<id>"""
        url = reverse('breed-detail', args=[self.breed1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Дворняжка")

    def test_update_breed(self):
        """Тест PUT /api/breeds/<id>"""
        url = reverse('breed-detail', args=[self.breed1.id])
        data = {
            "name": "Лабрадор",
            "size": "Large",
            "friendliness": 5,
            "trainability": 4,
            "shedding_amount": 3,
            "exercise_needs": 4
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.breed1.refresh_from_db()
        self.assertEqual(self.breed1.name, "Лабрадор")

    def test_delete_breed(self):
        """Тест DELETE /api/breeds/<id>"""
        url = reverse('breed-detail', args=[self.breed2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Breed.objects.count(), 1)
        with self.assertRaises(Breed.DoesNotExist):
            Breed.objects.get(id=self.breed2.id)
