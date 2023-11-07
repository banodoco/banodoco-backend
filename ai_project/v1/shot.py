from rest_framework.views import APIView
from ai_project.models import InternalFileObject, Project, Shot, Timing
from ai_project.v1.serializers.dao import AddShotClipDao, CreateShotDao, FetchShotDao, ShotListFilterDao, UUIDDao, UpdateShotDao
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
        if not ('name' in attributes.data and attributes.data['name']):
            attributes._data['name'] = "Shot " + str(shot_idx)
        else:
            prev_shot = Shot.objects.filter(project_id=project.id, name=attributes.data['name'], is_disabled=False).first()
            if prev_shot:
                return success({}, 'shot name already exists', False)

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
        
        if 'name' in attributes.data and attributes.data['name']: 
            prev_shot = Shot.objects.filter(project_id=shot.project.id, name=attributes.data['name'], is_disabled=False).first()
            if prev_shot:
                return success({}, 'shot name already exists', False)
        
        if 'main_clip_id' in attributes.data and attributes.data['main_clip_id']:
            video_clip = InternalFileObject.objects.filter(uuid=attributes.data['main_clip_id'], is_disabled=False).first()
            if not video_clip:
                return success({}, 'invalid video clip uuid', False)
            attributes._data['main_clip_id'] = video_clip.id
        
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

class ShotClipView(APIView):
    @auth_required('user', 'admin')
    def post(self, request):
        attributes = AddShotClipDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        shot = Shot.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not shot:
            return success({}, 'invalid shot uuid', False)
        
        video_clip = InternalFileObject.objects.filter(uuid=attributes.data['interpolated_clip_id'], is_disabled=False).first()
        if not video_clip:
            return success({}, 'invalid video clip uuid', False)

        shot.add_interpolated_clip_list([video_clip.uuid.hex])
        shot.save()

        return success({}, 'shot clip added successfully', True)
    
class ShotDuplicateView(APIView):
    @auth_required('user', 'admin')
    def post(self, request):
        attributes = UUIDDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        shot: Shot = Shot.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not shot:
            return success({}, 'invalid shot uuid', False)
        
        shot_number = Shot.objects.filter(project_id=shot.project.id, is_disabled=False).count() + 1
        shot_data = {
            "name" : shot.name + " (copy)",
            "desc" : shot.desc,
            "shot_idx" : shot_number,
            "duration" : shot.duration,
            "meta_data" : shot.meta_data,
            "project_id" : shot.project.id
        }

        new_shot = Shot.objects.create(**shot_data)
        
        timing_list = Timing.objects.filter(shot_id=shot.id, is_disabled=False).all()
        new_timing_list = []
        for timing in timing_list:
            data = {
                "model_id": timing.model_id,
                "source_image_id": timing.source_image_id,
                "mask_id": timing.mask_id,
                "canny_image_id": timing.canny_image_id,
                "primary_image_id": timing.primary_image_id,
                "shot_id": new_shot.id,
                "alternative_images": timing.alternative_images,
                "notes": timing.notes,
                "clip_duration": timing.clip_duration,
                "aux_frame_index": timing.aux_frame_index,
            }

            new_timing = Timing.objects.create(**data)
            new_timing_list.append(new_timing)
        
        context = {'timing_list': new_timing_list}
        
        payload = {
            'data': ShotDto(new_shot, context=context).data
        }

        return success(payload, 'shot duplicated successfully', True)

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

        if 'project_id' in attributes.data and attributes.data['project_id']:
            project: Project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project uuid', False)
            
            attributes._data['project_id'] = project.id

        print(attributes.data)
        attributes._data['is_disabled'] = False
        
        self.shot_list = Shot.objects.filter(**attributes.data).order_by('shot_idx').all()
        timing_list = Timing.objects.filter(is_disabled=False).all()
        if 'project_id' in attributes.data:
            timing_list = timing_list.filter(shot__project_id=attributes.data['project_id'])
        context = {'timing_list': timing_list}

        paginator = Paginator(self.shot_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": ShotDto(paginator.page(page), many=True, context=context).data,
        }

        return success(payload, "timing list fetched successfully", True)