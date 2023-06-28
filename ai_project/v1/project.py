from rest_framework.views import APIView
from ai_project.models import Project
from ai_project.v1.serializers.dao import CreateProjectDao, ProjectFilterDao, UUIDDao, UpdateProjectDao
from ai_project.v1.serializers.dto import ProjectDto
from django.core.paginator import Paginator

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType
from user.models import User

class ProjectAPIView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        payload = {
            'data': ProjectDto(project).data
        }

        return success(payload, 'successfully fetched project', True)
    
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = CreateProjectDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        user_id = attributes.data['user_id'] if request.role_type == UserType.ADMIN.value else request.role_id
        user = User.objects.filter(uuid=user_id, is_disabled=False).first()
        if not user:
            return success({}, 'invalid user uuid', False)
        
        print(attributes.data)
        attributes._data['user_id'] = user.id

        project = Project.objects.create(**attributes.data)

        payload = {
            'data': ProjectDto(project).data
        }

        return success(payload, 'successfully created project', True)
    
    @auth_required('admin', 'user')
    def put(self, request):
        attributes = UpdateProjectDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        if project.user_id != request.role_id and request.role_type != UserType.ADMIN.value:
            return unauthorized({})
        
        for k,v in attributes.data.items():
            setattr(project, k, v)

        project.save()

        payload = {
            'data': ProjectDto(project).data
        }

        return success(payload, 'successfully updated project', True)
    
    @auth_required('admin', 'user')
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        if project.user_id != request.role_id and request.role_type != UserType.ADMIN.value:
            return unauthorized({})
        
        project.is_disabled = True
        project.save()

        return success({}, 'successfully deleted project', True)
    

class  ProjectListAPIView(APIView):
    def __init__(self):
        self.project_list = []
        
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = ProjectFilterDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        page = attributes.data['page']
        del attributes._data['page']
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        user_id = attributes.data['user_id'] if request.role_type == UserType.ADMIN.value else request.role_id
        user = User.objects.filter(uuid=user_id, is_disabled=False).first()
        if not user:
            return success({}, 'invalid user uuid', False)
        
        print(attributes.data)
        attributes._data['user_id'] = user.id
        attributes._data['is_disabled'] = False
        
        self.project_list = Project.objects.filter(**attributes.data).all()

        paginator = Paginator(self.project_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": ProjectDto(
                paginator.page(page), many=True
            ).data,
        }
        return success(payload, "project list fetched successfully", True)