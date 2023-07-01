import json
import time
from rest_framework.views import APIView
from middleware.response import success
from payment.constants import PaymentOrderStatus
from payment.models import PaymentOrder

from util.payment.stripe import Stripe
from util.payment.stripe_constants import StripeEvent

# TODO: add parameter in nginx for the stripe signature
class WebhookView(APIView):
    # @csrf_exempt
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        
        stripe_client = Stripe()
        event = stripe_client.validate_event(payload, sig_header)

        if event:
            if event.type in [StripeEvent.INVOICE_PAYMENT_SUCCESS, StripeEvent.INVOICE_PAYMENT_FAILED]:
                order_id = event.data.object.metadata['order_id']
                if order_id:
                    order = PaymentOrder.objects.get(uuid=order_id, is_disabled=False).first()
                    if order:
                        order.status = PaymentOrderStatus.COMPLETED.value if event.type == \
                            StripeEvent.INVOICE_PAYMENT_SUCCESS else PaymentOrderStatus.FAILED.value
                        order.payment_updated_on = time.time()
                        order.transaction_data = json.dumps(event)
                        order.save()


        return success({}, 'webhook success', True)

        
        