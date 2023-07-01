import random
import string
from django.db import models

from banodoco.base_model import BaseModel
from payment.constants import PAYMENT_ORDER_IDENTIFIER_LENGTH, PaymentOrderStatus
from user.models import User

def get_unique_identifier():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(PAYMENT_ORDER_IDENTIFIER_LENGTH))

class PaymentOrder(BaseModel):
    identifier = models.CharField(max_length=100, default=get_unique_identifier)
    name = models.CharField(max_length=100)
    total_credits = models.FloatField(default=0)
    total_amount_usd = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default=PaymentOrderStatus.PENDING.value)
    payment_updated_on = models.DateTimeField(null=True)
    transaction_data = models.TextField(null=True)

    class Meta:
        db_table = 'order'