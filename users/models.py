from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=55)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Gender(models.TextChoices):
        ME = 'Male'
        FE = 'Female'

    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    phone_number = models.CharField(max_length=14, blank=True, null=True)
    postall_address = models.PositiveIntegerField(default=100000, null=True, blank=True)

    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.FE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    workplace = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=55,  null=True, blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
