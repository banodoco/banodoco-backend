from rest_framework.views import APIView
from banodoco.settings import AMOUNT_TO_CREDITS_MULTIPLIER
from middleware.authentication import auth_required
from middleware.response import bad_request, success
from payment.models import PaymentOrder
from payment.v1.serializers.dao import GeneratePaymentLinkDao
from user.models import User

from util.payment.stripe import Stripe

class PaymentView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = GeneratePaymentLinkDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        user = User.objects.filter(uuid=request.role_id, is_disabled=False).first()
        if not user:
            return success({}, 'invalid user', True)
        
        order_data = {
            "name" : 'Banodoco Credits',
            "total_credits" : attributes.data['total_amount'] * AMOUNT_TO_CREDITS_MULTIPLIER,
            "total_amount_usd" : attributes.data['total_amount'],
            "user_id" : user.id,
            "is_paid" : False
        }
        order = PaymentOrder.objects.create(**order_data)

        stripe_client = Stripe()
        payment_link = stripe_client.create_payment_link(order)

        payload = {
            'data': payment_link
        }

        return success(payload, 'payment link generated successfully', True)