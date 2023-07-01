from rest_framework import serializers

class  GeneratePaymentLinkDao(serializers.Serializer):
    total_amount = serializers.IntegerField(default=10)

class OrderListFilterDao(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=False)
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)

class UUIDDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)