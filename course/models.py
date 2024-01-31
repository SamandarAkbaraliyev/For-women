from django.db import models
from main.models import BaseModel


class Course(BaseModel):
    title = models.CharField(max_length=55)
