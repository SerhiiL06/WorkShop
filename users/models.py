from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_master = models.BooleanField(default=False)


class Specific(models.Model):
    SKILLS_CHOISE = (
        ("IT", "IT technology"),
        ("Computer", "Computer service"),
        ("Plumbing", "Plumbing service"),
        ("Electician", "Electrician service"),
    )

    master = models.ManyToManyField(
        User,
        related_name="specific",
        limit_choices_to={"is_master": "True"},
    )
    skills = models.CharField(choices=SKILLS_CHOISE, max_length=15)
