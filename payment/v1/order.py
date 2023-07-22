from rest_framework.views import APIView

from middleware.authentication import auth_required
from middleware.response import bad_request, success
from payment.models import PaymentOrder
from payment.v1.serializers.dao import OrderListFilterDao, UUIDDao
from payment.v1.serializers.dto import PaymentOrderDetailDto, PaymentOrderDto
from user.constants import UserType
from django.core.paginator import Paginator

class OrderView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        order = PaymentOrder.objects.filter(id=attributes.data["uuid"]).first()
        if not order:
            return success({}, "order not found", False)
        
        if order.user.uuid != request.role_id and request.role_type != UserType.ADMIN.value:
            return success({}, "unauthorized", False)
        
        payload = {
            'data': PaymentOrderDetailDto(order).data,
        }

        return success(payload, "order fetched successfully", True)

class OrderListView(APIView):
    def __init__(self):
        self.order_list = []

    @auth_required("admin", "user")
    def get(self, request):
        attributes = OrderListFilterDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        page = attributes.data["page"]
        del attributes._data["page"]
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        self.order_list = PaymentOrder.objects.all()

        print(attributes.data)
        user_id = attributes.data['user_id'] if 'user_id' in attributes.data and \
            attributes.data['user_id'] and request.role_type == UserType.ADMIN.value else request.role_id
        
        attributes._data["user_id"] = user_id
        attributes._data["is_disabled"] = False

        self.order_list = self.order_list.filter(**attributes.data)

        paginator = Paginator(self.order_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)

        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": PaymentOrderDto(paginator.page(page), many=True).data,
        }
        return success(payload, "file list fetched successfully", True)
