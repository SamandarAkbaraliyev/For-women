from django.db import models
from users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Category(BaseModel):
    name = models.CharField(max_length=55)

    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=55)

    def __str__(self) -> str:
        return self.name


class Contact(BaseModel):
    name = models.CharField(max_length=55)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=55)
    content = models.TextField(null=True)


class Report(BaseModel):
    class Complaint(models.TextChoices):
        NO = "Noo'rin savol/izoh"
        IN = "Insonning sha'niga teguvchi gaplar"
        BO = "Boshqalarga nisbatan so'kish"
        TE = "Terrorizmga da'vat"
        TU = "Tushunarsiz va umuman kerak bo'lmagan izoh"

    complaint = models.CharField(max_length=100, choices=Complaint.choices, default=Complaint.NO, null=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.complaint
