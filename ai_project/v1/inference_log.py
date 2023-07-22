from rest_framework.views import APIView
from ai_project.models import AIModel, InferenceLog, Project
from ai_project.v1.serializers.dao import (
    CreateInferenceLogDao,
    InferenceLogListFilterDao,
    UUIDDao,
    UpdateInferenceLogDao,
)
from ai_project.v1.serializers.dto import InferenceLogDto
from django.core.paginator import Paginator

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType


class InferenceLogView(APIView):
    @auth_required("admin", "user")
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        log = InferenceLog.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not log:
            return success({}, "invalid log uuid", False)

        payload = {
            "data": InferenceLogDto(log).data,
        }

        return success(payload, "successfully fetched log", True)

    @auth_required("admin", "user")
    def post(self, request):
        attributes = CreateInferenceLogDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        print(attributes.data)

        if "project_id" in attributes.data and attributes.data["project_id"]:
            project = Project.objects.filter(
                uuid=attributes.data["project_id"], is_disabled=False
            ).first()
            if not project:
                return success({}, "invalid project", False)

            if (
                str(project.user.uuid).replace('-','') != request.role_id
                and request.role_type != UserType.ADMIN.value
            ):
                return unauthorized({})

            attributes._data["project_id"] = project.id

        if "model_id" in attributes.data and attributes.data["model_id"]:
            model = AIModel.objects.filter(
                uuid=attributes.data["model_id"], is_disabled=False
            ).first()
            if not model:
                return success({}, "invalid model", False)

            attributes._data["model_id"] = model.id

        log = InferenceLog.objects.create(**attributes.data)

        payload = {"data": InferenceLogDto(log).data}

        return success(payload, "inference log created successfully", True)

    @auth_required("admin", "user")
    def put(self, request):
        attributes = UpdateInferenceLogDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        log = InferenceLog.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not log:
            return success({}, "invalid log uuid", False)

        print(attributes.data)
        if "project_id" in attributes.data and attributes.data["project_id"]:
            project = Project.objects.filter(
                uuid=attributes.data["project_id"], is_disabled=False
            ).first()
            if not project:
                return success({}, "invalid project", False)

            if (
                str(project.user.uuid).replace('-','') != request.role_id
                and request.role_type != UserType.ADMIN.value
            ):
                return unauthorized({})

            attributes._data["project_id"] = project.id

        if "model_id" in attributes.data and attributes.data["model_id"]:
            model = AIModel.objects.filter(
                uuid=attributes.data["model_id"], is_disabled=False
            ).first()
            if not model:
                return success({}, "invalid model", False)

            attributes._data["model_id"] = model.id

        for k, v in attributes.data.items():
            setattr(log, k, v)

        log.save()

        payload = {"data": InferenceLogDto(log).data}

        return success(payload, "inference log updated successfully", True)

    @auth_required("admin", "user")
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        log = InferenceLog.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not log:
            return success({}, "invalid log uuid", False)

        log.is_disabled = True
        log.save()

        return success({}, "inference log deleted successfully", True)


class InferenceLogListView(APIView):
    def __init__(self):
        self.log_list = []

    @auth_required("admin", "user")
    def get(self, request):
        attributes = InferenceLogListFilterDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        page = attributes.data["page"]
        del attributes._data["page"]
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        print(attributes.data)
        if "project_id" in attributes.data:
            project = Project.objects.filter(
                uuid=attributes.data["project_id"], is_disabled=False
            ).first()
            if not project:
                return success({}, "invalid project", False)

            if (
                str(project.user.uuid).replace('-','') != request.role_id
                and request.role_type != UserType.ADMIN.value
            ):
                return unauthorized({})

            attributes._data["project_id"] = project.id

        if "model_id" in attributes.data and attributes.data["model_id"]:
            model = AIModel.objects.filter(
                uuid=attributes.data["model_id"], is_disabled=False
            ).first()
            if not model:
                return success({}, "invalid model", False)

            attributes._data["model_id"] = model.id

        attributes._data["is_disabled"] = False

        self.log_list = InferenceLog.objects.filter(**attributes.data).all()

        paginator = Paginator(self.log_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)

        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": InferenceLogDto(paginator.page(page), many=True).data,
        }
        return success(payload, "log list fetched successfully", True)
