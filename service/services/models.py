from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()


class Plan(models.Model):
    PLAN_TYPES = (
        ('Full', 'full'),
        ('Student', 'student'),
        ('Discount', 'discount'),
    )

    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(100)
    ])


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
