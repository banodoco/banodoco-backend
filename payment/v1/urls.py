from django.conf.urls import url

from payment.v1.order import OrderListView, OrderView
from payment.v1.webhook import WebhookView

urlpatterns = [
    # timing
    url(r'^order$', OrderView.as_view()),
    url(r'^order/list$', OrderListView.as_view()),
    url(r'^stripe-webhook$', WebhookView.as_view()),
]