from rest_framework import serializers

from services.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.company')
    email = serializers.CharField(source='client.user.email')

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client', 'email')
