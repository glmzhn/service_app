from django.db.models import Prefetch, F
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company', 'user__email'))
    ).annotate(price=F('service__price') -
                     F('service__price') *
                     F('plan__discount_percentage') / 100.00)
    serializer_class = SubscriptionSerializer
