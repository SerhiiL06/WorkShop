from django.db import models
from users.models import User


class Category(models.Model):
    service = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.service


class Order(models.Model):
    STATUS_ORDER = (
        ("in process", "in processing"),
        ("assigned", "assigned to the master"),
        ("rej", "rejected"),
        ("complete", "complete"),
    )

    status = models.CharField(choices=STATUS_ORDER, max_length=10, default="in process")

    created = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    meeting_time = models.DateTimeField(null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=500, null=True)

    master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_master": "True"},
        related_name="tasks",
        null=True,
    )
