import json
from rest_framework import serializers

from payment.models import PaymentOrder
from user.v1.serializers.dto import UserDto

class PaymentOrderDto(serializers.ModelSerializer):
    
    class Meta:
        model = PaymentOrder
        fields = ("uuid", "created_on", "identifier", "name","total_credits","total_amount_usd", "status","payment_updated_on")


class PaymentOrderDetailDto(serializers.ModelSerializer):
    transaction_data = serializers.SerializerMethodField()
    user = UserDto()

    class Meta:
        model = PaymentOrder
        fields = ("uuid", "created_on", "identifier" "name","total_credits","total_amount_usd", \
                  "user","status","payment_updated_on", "transaction_data")
        
    def get_transaction_data(self, obj):
        return json.loads(obj.transaction_data) if obj.transaction_data else None