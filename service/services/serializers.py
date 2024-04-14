from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client = serializers.CharField(source='client.company')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return (instance.service.price -
                instance.service.price *
                (instance.plan.discount_percentage / 100))

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client', 'email', 'plan', 'price')
