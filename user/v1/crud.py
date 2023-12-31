from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from authentication.v1.serializers.dto import UserDto
from middleware.authentication import auth_required
from middleware.response import bad_request, success
from user.models import User
from user.v1.serializers.dao import CreateUserDao, GetUserDao, UpdateUserDao, UserListFilterDao


class UserView(APIView):
    @auth_required('admin')
    def post(self, request):
        attributes = CreateUserDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        user = User.objects.filter(email=attributes.data['email'], is_disabled=False).first()
        if user:
            return success({}, 'user already exists', False)
        
        attributes._data['password'] = make_password(attributes.data['password'])
        
        user = User.objects.create(**attributes.data)

        payload = {
            'data': UserDto(user).data
        }
        
        return success(payload, "user created successfully", True)
    

    @auth_required('admin', 'user')
    def put(self, request):
        attributes = UpdateUserDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        if 'uuid' in attributes.data and attributes.data['uuid']:
            user = User.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        else:
            user = User.objects.filter(uuid=request.role_id, is_disabled=False).first()
            
        if not user:
            return success({}, 'invalid user uuid', False)
        
        if request.role_type == 'user' and user.uuid.hex != request.role_id:
            return success({}, 'invalid user', False)
        
        # if email already exists for another user then return error
        if 'email' in attributes.data:
            user_with_email = User.objects.filter(email=attributes.data['email'], is_disabled=False)\
                .exclude(uuid=attributes.data['uuid']).first()
            if user_with_email and user_with_email.uuid.hex != user.uuid.hex:
                return success({}, 'email already exists', False)
        
        if 'credits_to_add' in attributes.data:
            attributes._data['total_credits'] = max(user.total_credits + attributes._data['credits_to_add'], 0)

        for attr, value in attributes.data.items():
            setattr(user, attr, value)
        
        user.save()

        payload = {
            'data': UserDto(user).data
        }

        return success(payload, 'user updated successfully', True)
    

    @auth_required('admin', 'user')
    def get(self, request):
        attributes = GetUserDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        request_user = User.objects.filter(uuid=request.role_id, is_disabled=False).first()
        if not request_user:
            return success({}, 'invalid user', False)
        
        user = None
        if 'uuid' in attributes.data and attributes.data['uuid']:
            user = User.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        elif 'email' in attributes.data and attributes.data['email']:
            user = User.objects.filter(email=attributes.data['email'], is_disabled=False).first()
        
        # TODO: hackish way of fetching the current user, will update later
        if not user:
            user = request_user
        
        if not (request_user.id == user.id or request.role_type == 'admin'):
            return success({}, "unauthorized", False)
        
        payload = {
            'data': UserDto(user).data
        }

        return success(payload, "user fetched successfully", True)
    

class UserListView(APIView):
    def __init__(self):
        self.user_list = []

    @auth_required("admin", "user")
    def get(self, request):
        attributes = UserListFilterDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        page = attributes.data["page"]
        del attributes._data["page"]
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        self.user_list = User.objects.all()

        print(attributes.data)
        attributes._data["is_disabled"] = False

        self.user_list = self.user_list.filter(**attributes.data)

        paginator = Paginator(self.user_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)

        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": UserDto(paginator.page(page), many=True).data,
        }
        return success(payload, "file list fetched successfully", True)
