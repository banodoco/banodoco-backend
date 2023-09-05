import stripe
from ai_project.constants import ServerType

from banodoco.settings import SERVER, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from payment.models import PaymentOrder
from util.payment.stripe_constants import TEST_USD_01_BANODOCO_CREDITS, USD_01_BANODOCO_CREDITS


class Stripe:
    def __init__(self):
        self.client = stripe
        self.client.api_key = STRIPE_SECRET_KEY

    def create_payment_link(self, order: PaymentOrder, quantity = 1):
        price = TEST_USD_01_BANODOCO_CREDITS if SERVER == ServerType.DEVELOPMENT.value else USD_01_BANODOCO_CREDITS
        payment_obj = self.client.PaymentLink.create(
                line_items=[{"price": price, "quantity": quantity}],
                after_completion={"type": "redirect", "redirect": {"url": "https://payment.banodoco.ai"}},
                invoice_creation={
                    "enabled": True,
                    "invoice_data": {
                        "description": "Invoice for Banodoco Credits",
                        "metadata": {"order_identifier": order.identifier, "order_id": order.uuid},
                        "custom_fields": [{"name": "email", "value": order.user.email}],
                        "footer": "Banodoco Inc.",
                    },
                },
                automatic_tax={"enabled": True},
                metadata={'order_id': str(order.uuid)}
            )
        
        print('payment obj')
        print(payment_obj)
        if 'url' in payment_obj:
            return payment_obj['url']
        
        return None
    
    # TODO: handle invalidated events, maybe send them to slack for inspection
    def validate_event(self, payload, sig_header):
        try:
            event = self.client.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )

            return event
        except ValueError as e:
            return None