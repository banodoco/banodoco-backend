from rest_framework.views import APIView
from django.db import models
from django.core.paginator import Paginator
from ai_project.models import InternalFileObject, Project
from ai_project.v1.serializers.dao import (
    CreateFileDao,
    FileListFilterDao,
    UUIDDao,
    UpdateFileDao,
)
from ai_project.v1.serializers.dto import InternalFileDto

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType


class FileView(APIView):
    @auth_required("admin", "user")
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        file = InternalFileObject.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not file:
            return success({}, "invalid file uuid", False)

        if file.project:
            if (
                file.project.user.uuid != request.role_id
                and request.role_id != UserType.ADMIN.value
            ):
                return unauthorized({})

        payload = {
            "data": InternalFileDto(file).data,
        }

        return success(payload, "success", True)

    @auth_required("admin", "user")
    def update(self, request):
        attributes = UpdateFileDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        file = InternalFileObject.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not file:
            return success({}, "invalid file uuid", False)

        if file.project:
            if (
                file.project.user.uuid != request.role_id
                and request.role_id != UserType.ADMIN.value
            ):
                return unauthorized({})

        if "project_id" in attributes.data:
            project = Project.objects.filter(
                uuid=attributes.data["project_id"], is_disabled=False
            ).first()
            if not project:
                return success({}, "invalid project uuid", False)

            print(attributes.data)
            attributes._data["project_id"] = project.id

        for k, v in attributes.data.items():
            setattr(file, k, v)

        file.save()

        payload = {
            "data": InternalFileDto(file).data,
        }

        return success(payload, "success", True)

    @auth_required("admin", "user")
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        file = InternalFileObject.objects.filter(
            uuid=attributes.data["uuid"], is_disabled=False
        ).first()
        if not file:
            return success({}, "invalid file uuid", False)

        if file.project:
            if (
                file.project.user.uuid != request.role_id
                and request.role_id != UserType.ADMIN.value
            ):
                return unauthorized({})

        file.is_disabled = True
        file.save()

        return success({}, "success", True)

    @auth_required("admin", "user")
    def post(self, request):
        attributes = CreateFileDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        if "project_id" in attributes.data and attributes.data["project_id"]:
            project = Project.objects.filter(
                uuid=attributes.data["project_id"], is_disabled=False
            ).first()
            if not project:
                return success({}, "invalid project", False)

            print(attributes.data)
            attributes._data["project_id"] = project.id

        file = InternalFileObject.objects.create(**attributes.data)

        payload = {
            "data": InternalFileDto(file).data,
        }

        return success(payload, "success", True)


class FileListView(APIView):
    def __init__(self):
        self.file_list = []

    @auth_required("admin", "user")
    def get(self, request):
        attributes = FileListFilterDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        page = attributes.data["page"]
        del attributes._data["page"]
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        self.file_list = InternalFileObject.objects.all()

        print(attributes.data)
        if "project_id" in attributes.data:
            project_id = attributes.data["project_id"]
            project = Project.objects.filter(uuid=project_id, is_disabled=False).first()
            if not project:
                return success({}, "invalid project", False)

            attributes._data["project_id"] = project.id

        attributes._data["is_disabled"] = False

        self.file_list = self.file_list.filter(**attributes.data)

        paginator = Paginator(self.file_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)

        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": InternalFileDto(paginator.page(page), many=True).data,
        }
        return success(payload, "file list fetched successfully", True)
