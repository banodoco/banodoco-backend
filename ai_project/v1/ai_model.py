import json

from rest_framework.views import APIView
from ai_project.models import AIModel
from ai_project.v1.serializers.dao import (
    AIModelListFilterDao,
    CreateAIModelDao,
    GetAIModelDao,
    UUIDDao,
    UpdateAIModelDao,
)
from ai_project.v1.serializers.dto import AIModelDto
from django.core.paginator import Paginator

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType
from user.models import User


class AIModelView(APIView):
    @auth_required("admin", "user")
    def get(self, request):
        attributes = GetAIModelDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        if ('user_id' in attributes.data and attributes.data['user_id']) and \
            (str(request.role_id).replace('-', '') != attributes.data['user_id'].replace('-', '') and request.role_type != UserType.ADMIN.value):
            return unauthorized({})
        
        current_user_uuid = attributes.data['user_id'] if 'user_id' in attributes.data else request.role_id
        current_user = User.objects.filter(uuid=current_user_uuid, is_disabled=False).first()
        if not current_user:
            return unauthorized({})

        if 'uuid' in attributes.data and attributes.data['uuid']:
            ai_model = AIModel.objects.filter(
                uuid=attributes.data["uuid"], user_id=current_user.id, is_disabled=False
            ).first()
        else:
            ai_model = AIModel.objects.filter(replicate_url=attributes.data['replicate_url'], user_id=current_user.id, is_disabled=False).first()

        if not ai_model:
            return success({}, "invalid model uuid", False)

        payload = {"data": AIModelDto(ai_model).data}

        return success(payload, "successfully fetched the model", True)

    @auth_required("admin", "user")
    def post(self, request):
        attributes = CreateAIModelDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        print(attributes.data)

        user_id = attributes.data["user_id"]\
            if request.role_type == UserType.ADMIN.value and 'user_id' in attributes.data \
            else request.role_id

        user = User.objects.filter(uuid=user_id, is_disabled=False).first()
        if not user:
            return success({}, "invalid user", False)

        print(attributes.data)
        attributes._data["user_id"] = user.id

        ai_model = AIModel.objects.create(**attributes.data)

        payload = {"data": AIModelDto(ai_model).data}

        return success(payload, "ai_model fetched", True)

    @auth_required("admin", "user")
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        ai_model = AIModel.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not ai_model:
            return success({}, "invalid model uuid", False)

        if (
            str(ai_model.user.uuid).replace('-','') != request.role_id
            and request.role_type != UserType.ADMIN.value
        ):
            return unauthorized({})

        ai_model.is_disabled = True
        ai_model.save()

        return success({}, "ai_model deleted", True)

    @auth_required("admin", "user")
    def put(self, request):
        attributes = UpdateAIModelDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        ai_model = AIModel.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not ai_model:
            return success({}, "invalid model uuid", False)

        if (
            str(ai_model.user.uuid).replace('-','') != request.role_id
            and request.role_type != UserType.ADMIN.value
        ):
            return unauthorized({})

        user_id = attributes.data["user_id"]\
            if request.role_type == UserType.ADMIN.value and 'user_id' in attributes.data \
            else request.role_id
        if user_id:
            user = User.objects.filter(
                uuid=user_id, is_disabled=False
            ).first()
            if not user:
                return success({}, "invalid user", False)

            print(attributes.data)
            attributes._data["user_id"] = user.id

        for attr, value in attributes.data.items():
            setattr(ai_model, attr, value)
        ai_model.save()

        payload = {"data": AIModelDto(ai_model).data}

        return success(payload, "ai_model fetched", True)

class AIModelListView(APIView):
    def __init__(self):
        self.ai_model_list = []

    @auth_required("admin", "user")
    def get(self, request):
        attributes = AIModelListFilterDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        page = attributes.data["page"]
        del attributes._data["page"]
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        self.ai_model_list = AIModel.objects.all()

        user_id = attributes.data["user_id"]\
            if request.role_type == UserType.ADMIN.value and 'user_id' in attributes.data \
            else request.role_id
        user = User.objects.filter(uuid=user_id, is_disabled=False).first()
        if not user:
            return success({}, "invalid user uuid", False)

        print(attributes.data)
        attributes._data["user_id"] = user.id
        attributes._data["is_disabled"] = False

        if attributes.data['custom_trained'] == "all":
            del  attributes._data['custom_trained']
        elif attributes.data["custom_trained"] == "user":
            attributes._data["custom_trained"] = True
        else:
            attributes._data["custom_trained"] = False

        model_category_list, model_type_list = None, None
        if 'model_category_list' in attributes.data and attributes.data['model_category_list']:
            model_category_list = attributes.data['model_category_list']
            del attributes._data['model_category_list']
        
        if 'model_type_list' in attributes.data and attributes.data['model_type_list']:
            model_type_list = attributes.data['model_type_list']
            del attributes._data['model_type_list']


        self.ai_model_list = AIModel.objects.filter(**attributes.data).all()

        filtered_list = []
        for model in self.ai_model_list:
            category_check = True if (not model_category_list or (model_category_list and model.category in model_category_list)) else False
            type_check = True if (not model_type_list or (model_type_list and any(item in model_type_list for item in json.loads(model.model_type)))) else False

            if category_check and type_check:
                filtered_list.append(model)

        self.ai_model_list = filtered_list
        
        paginator = Paginator(self.ai_model_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)

        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": AIModelDto(paginator.page(page), many=True).data,
        }
        return success(payload, "model list fetched successfully", True)
