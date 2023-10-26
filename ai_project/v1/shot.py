from rest_framework.views import APIView
from ai_project.models import Project, Shot, Timing
from ai_project.v1.serializers.dao import CreateShotDao, FetchShotDao, ShotListFilterDao, UUIDDao, UpdateShotDao
from ai_project.v1.serializers.dto import ShotDto
from django.core.paginator import Paginator

from middleware.authentication import auth_required
from middleware.response import bad_request, success

class ShotCRUDView(APIView):
    @auth_required('user', 'admin')
    def get(self, request):
        attributes = FetchShotDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        if 'uuid' in attributes.data and attributes.data['uuid']:
            shot = Shot.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
            if not shot:
                return success({}, 'invalid shot uuid', False)
        elif 'project_id' in attributes.data and attributes.data['project_id']:
            project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project uuid', False)
            
            shot = Shot.objects.filter(project_id=project.id, shot_idx=attributes.data['shot_idx'], is_disabled=False).first()

        payload = {
            'data': ShotDto(shot).data
        }

        return success(payload, 'shot fetched successfully', True)
    
    @auth_required('user', 'admin')
    def post(self, request):
        attributes = CreateShotDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        print(attributes.data)
        attributes._data['project_id'] = project.id
        
        shot_idx = Shot.objects.filter(project_id=project.id, is_disabled=False).count() + 1
        attributes._data['shot_idx'] = shot_idx

        shot = Shot.objects.create(**attributes.data)
        
        timing_list = Timing.objects.filter(is_disabled=False).all()
        context = {'timing_list': timing_list}
        
        payload = {
            'data': ShotDto(shot, context=context).data
        }

        return success(payload, 'shot created successfully', True)
    
    @auth_required('user', 'admin')
    def put(self, request):
        attributes = UpdateShotDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        shot = Shot.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not shot:
            return success({}, 'invalid shot uuid', False)
        
        for k,v in attributes.data.items():
            setattr(shot, k, v)
        shot.save()
        
        timing_list = Timing.objects.filter(is_disabled=False).all()
        context = {'timing_list': timing_list}
        
        payload = {
            'data': ShotDto(shot, context=context).data
        }

        return success(payload, 'shot updated successfully', True)
    
    @auth_required('user', 'admin')
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        shot = Shot.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not shot:
            return success({}, 'invalid shot uuid', False)
        
        shot.is_disabled = True
        shot.save()
        
        return success({}, 'shot deleted successfully', True)
    

class ShotListView(APIView):
    def __init__(self):
        self.data_per_page = 10
        self.shot_list = []

    @auth_required('admin', 'user')
    def get(self, request):
        attributes = ShotListFilterDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        page = attributes.data['page']
        del attributes._data['page']
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        print(attributes.data)
        attributes._data['is_disabled'] = False
        
        self.shot_list = Shot.objects.filter(**attributes.data).order_by('aux_frame_index').all()

        paginator = Paginator(self.shot_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": ShotDto(paginator.page(page), many=True).data,
        }

        return success(payload, "timing list fetched successfully", True)