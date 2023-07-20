from rest_framework.views import APIView
from ai_project.models import AIModel, InternalFileObject, Project, Timing
from ai_project.v1.serializers.dao import CreateTimingDao, GetProjectTimingDao, GetTimingNumberDao, ShiftTimingDao, TimingListFilterDao, UUIDDao, UpdateTimingDao
from ai_project.v1.serializers.dto import TimingDto
from django.core.paginator import Paginator
from django.db.models import F

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType

class FrameTimingView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        timing = Timing.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        payload = {
            'data': TimingDto(timing).data,
        }

        return success(payload, 'successfully fetched timing', True)
    
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = CreateTimingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        print(attributes.data)
        
        if 'project_id' in attributes.data and attributes.data['project_id']:
            project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project id', False)
            
            if str(project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
                return unauthorized({})
            
            print(attributes.data)
            attributes._data['project_id'] = project.id
        
        if 'aux_frame_index' not in attributes.data or attributes.data['aux_frame_index'] == None: 
            attributes._data['aux_frame_index'] = Timing.objects.filter(project_id=attributes.data['project_id'], is_disabled=False).count()
        
        if 'model_id' in attributes.data:
            if attributes.data['model_id'] != None:
                model = AIModel.objects.filter(uuid=attributes.data['model_id'], is_disabled=False).first()
                if not model:
                    return success({}, 'invalid model uuid', False)
                
                attributes._data['model_id'] = model.id
        

        if 'source_image_id' in attributes.data:
            if attributes.data['source_image_id'] != None:
                source_image = InternalFileObject.objects.filter(uuid=attributes.data['source_image_id'], is_disabled=False).first()
                if not source_image:
                    return success({}, 'invalid source image uuid', False)
                
                attributes._data['source_image_id'] = source_image.id
        

        if 'interpolated_clip_id' in attributes.data:
            if attributes.data['interpolated_clip_id'] != None:
                interpolated_clip = InternalFileObject.objects.filter(uuid=attributes.data['interpolated_clip_id'], is_disabled=False).first()
                if not interpolated_clip:
                    return success({}, 'invalid interpolated clip uuid', False)
                
                attributes._data['interpolated_clip_id'] = interpolated_clip.id
        

        if 'timed_clip_id' in attributes.data:
            if attributes.data['timed_clip_id'] != None:
                timed_clip = InternalFileObject.objects.filter(uuid=attributes.data['timed_clip_id'], is_disabled=False).first()
                if not timed_clip:
                    return success({}, 'invalid timed clip uuid', False)
                
                attributes._data['timed_clip_id'] = timed_clip.id
        

        if 'mask_id' in attributes.data:
            if attributes.data['mask_id'] != None:
                mask = InternalFileObject.objects.filter(uuid=attributes.data['mask_id'], is_disabled=False).first()
                if not mask:
                    return success({}, 'invalid mask uuid', False)
                
                attributes._data['mask_id'] = mask.id
        

        if 'canny_image_id' in attributes.data:
            if attributes.data['canny_image_id'] != None:
                canny_image = InternalFileObject.objects.filter(uuid=attributes.data['canny_image_id'], is_disabled=False).first()
                if not canny_image:
                    return success({}, 'invalid canny image uuid', False)
                
                attributes._data['canny_image_id'] = canny_image.id
        

        if 'preview_video_id' in attributes.data:
            if attributes.data['preview_video_id'] != None:
                preview_video = InternalFileObject.objects.filter(uuid=attributes.data['preview_video_id'], is_disabled=False).first()
                if not preview_video:
                    return success({}, 'invalid preview video uuid', False)
                
                attributes._data['preview_video_id'] = preview_video.id
        

        if 'primay_image_id' in attributes.data:
            if attributes.data['primay_image_id'] != None:
                primay_image = InternalFileObject.objects.filter(uuid=attributes.data['primay_image_id'], is_disabled=False).first()
                if not primay_image:
                    return success({}, 'invalid primary image uuid', False)
                
                attributes._data['primay_image_id'] = primay_image.id
        
        
        timing = Timing.objects.create(**attributes.data)
        
        payload = {
            'data': TimingDto(timing).data
        }
        
        return success(payload, 'timing created successfully', True)
    
    @auth_required('admin', 'user')
    def put(self, request):
        attributes = UpdateTimingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        timing = Timing.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        if 'primary_image_id' in attributes.data:
            if attributes.data['primary_image_id'] != None:
                primary_image: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['primary_image_id'], is_disabled=False).first()
                if not primary_image:
                    return success({}, 'invalid primary image uuid', False)
                
                attributes._data['primary_image_id'] = primary_image.id

        if 'model_id' in attributes.data:
            if attributes.data['model_id'] != None:
                model: AIModel = AIModel.objects.filter(uuid=attributes.data['model_id'], is_disabled=False).first()
                if not model:
                    return success({}, 'invalid model uuid', False)
                
                attributes._data['model_id'] = model.id
        

        if 'source_image_id' in attributes.data:
            if attributes.data['source_image_id'] != None:
                source_image: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['source_image_id'], is_disabled=False).first()
                if not source_image:
                    return success({}, 'invalid source image uuid', False)
                
                attributes._data['source_image_id'] = source_image.id
        

        if 'interpolated_clip_id' in attributes.data:
            if attributes.data['interpolated_clip_id'] != None:
                interpolated_clip: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['interpolated_clip_id'], is_disabled=False).first()
                if not interpolated_clip:
                    return success({}, 'invalid interpolated clip uuid', False)
                
                attributes._data['interpolated_clip_id'] = interpolated_clip.id
        

        if 'timed_clip_id' in attributes.data:
            if attributes.data['timed_clip_id'] != None:
                timed_clip: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['timed_clip_id'], is_disabled=False).first()
                if not timed_clip:
                    return success({}, 'invalid timed clip uuid', False)
                
                attributes._data['timed_clip_id'] = timed_clip.id
        

        if 'mask_id' in attributes.data:
            if attributes.data['mask_id'] != None:
                mask: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['mask_id'], is_disabled=False).first()
                if not mask:
                    return success({}, 'invalid mask uuid', False)
                
                attributes._data['mask_id'] = mask.id
        

        if 'canny_image_id' in attributes.data:
            if attributes.data['canny_image_id'] != None:
                canny_image: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['canny_image_id'], is_disabled=False).first()
                if not canny_image:
                    return success({}, 'invalid canny image uuid', False)
                
                attributes._data['canny_image_id'] = canny_image.id
        

        if 'preview_video_id' in attributes.data:
            if attributes.data['preview_video_id'] != None:
                preview_video: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['preview_video_id'], is_disabled=False).first()
                if not preview_video:
                    return success({}, 'invalid preview video uuid', False)
                
                attributes._data['preview_video_id'] = preview_video.id
        

        if 'primay_image_id' in attributes.data:
            if attributes.data['primay_image_id'] != None:
                primay_image: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['primay_image_id'], is_disabled=False).first()
                if not primay_image:
                    return success({}, 'invalid primary image uuid', False)
                
                attributes._data['primay_image_id'] = primay_image.id
        
        for attr, value in attributes.data.items():
            setattr(timing, attr, value)
        timing.save()

        payload = {}

        return success(payload, 'timing updated successfully', True)

    @auth_required('admin', 'user')
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        timing = Timing.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        timing.is_disabled = False
        timing.save()
        
        return success({}, 'timing deleted successfully', True)

class ProjectTimingView(APIView):
    # get timing from frame number and project
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = GetProjectTimingDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        timing = Timing.objects.filter(project=project, \
                    aux_frame_index=attributes.data['frame_number'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing', False)

        payload = {
            'data': TimingDto(timing).data
        }
        
        return success(payload, 'timings fetched successfully', True)
    
    # remove all timings of a project
    @auth_required('admin', 'user')
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project = Project.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        Timing.objects.filter(project=project, is_disabled=False).update(is_disabled=True)
        
        return success({}, 'timings deleted successfully', True)

# to get say 2 frames after a certain frame
class TimingNumberView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = GetTimingNumberDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        timing = Timing.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        res_timing = Timing.objects.filter(project=timing.project, \
                        aux_frame_index=timing.aux_frame_index + attributes.data['distance'], is_disabled=False).first()
        
        payload = {
            'data': TimingDto(res_timing).data if res_timing else None
        }

        return success(payload, 'timing fetched successfully', True)

# TODO: make this shifting more general depending on the usage
class ShiftTimingViewDao(APIView):
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = ShiftTimingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project: Project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project uuid', False)
        
        timing_list = Timing.objects.filter(project_id=project.id, \
                                            aux_frame_index__gte=attributes.data['index_of_frame'], is_disabled=False).order_by('frame_number')
        
        timing_list.update(aux_frame_index=F('aux_frame_index') + 1)

        return success({}, 'frames moved successfully', True)
    
class TimingListView(APIView):
    def __init__(self):
        self.timing_list = []
        
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = TimingListFilterDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        page = attributes.data['page']
        del attributes._data['page']
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        print(attributes.data)
        if 'project_id' in attributes.data and attributes.data['project_id']:
            project: Project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project uuid', False)
            
            if str(project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
                return unauthorized({})

            attributes._data['project_id'] = project.id
        
        attributes._data['is_disabled'] = False
        
        self.timing_list = Timing.objects.filter(**attributes.data).all()

        paginator = Paginator(self.timing_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": TimingDto(
                paginator.page(page), many=True
            ).data,
        }
        return success(payload, "timing list fetched successfully", True)