from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percentage = self.discount_percentage

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if not created and self.discount_percentage != self.__discount_percentage:
            self.update_subscriptions()

    def update_subscriptions(self):
        for subscription in self.subscriptions.all():
            set_price.delay(subscription.id)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
