from rest_framework.views import APIView
from ai_project.models import AIModel, InternalFileObject, Project, Timing, Shot
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
    
    def _clean_attributes(self, attributes, request_data):
        for k, v in attributes.data.items():
            if k not in request_data:
                del attributes._data[k]
    
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = CreateTimingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        self._clean_attributes(attributes, request.data)
        print(attributes.data)
        
        if 'shot_id' in attributes.data and attributes.data['shot_id']:
            shot = Shot.objects.filter(uuid=attributes.data['shot_id'], is_disabled=False).first()
            if not shot:
                return success({}, 'invalid shot id', False)
            
            if str(shot.project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
                return unauthorized({})
            
            attributes._data['shot_id'] = shot.id
        
        if 'aux_frame_index' not in attributes.data or attributes.data['aux_frame_index'] == None:
            attributes._data['aux_frame_index'] = Timing.objects.filter(shot_id=attributes.data['shot_id'], is_disabled=False).count()
        
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
        
        self._clean_attributes(attributes, request.data)

        timing = Timing.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        if 'primary_image_id' in attributes.data:
            if attributes.data['primary_image_id'] != None:
                primary_image: InternalFileObject = InternalFileObject.objects.filter(uuid=attributes.data['primary_image_id'], is_disabled=False).first()
                if not primary_image:
                    return success({}, 'invalid primary image uuid', False)
                
                attributes._data['primary_image_id'] = primary_image.id

        if 'shot_id' in attributes.data:
            if attributes.data['shot_id'] != None:
                shot: Shot = Shot.objects.filter(uuid=attributes.data['shot_id'], is_disabled=False).first()
                if not shot:
                    return success({}, 'invalid shot uuid', False)
                
                if str(shot.project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
                    return unauthorized({})
                
                attributes._data['shot_id'] = shot.id

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
        
        timing.is_disabled = True
        timing.save()
        
        return success({}, 'timing deleted successfully', True)

class ProjectTimingView(APIView):
    # get timing from frame number and project
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = GetProjectTimingDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        if 'project_id' in attributes.data:
            project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project uuid', False)
            
            shot_list = Shot.objects.filter(project_id=project.id, is_disabled=False).all()
            shot_id_list = [s.id for s in shot_list]
        
            timing = Timing.objects.filter(shot_id__in=shot_id_list, \
                        aux_frame_index=attributes.data['frame_number'], is_disabled=False).first()
        elif 'shot_id' in attributes.data:
            shot = Shot.objects.filter(uuid=attributes.data['shot_id'], is_disabled=False).first()
            if not shot:
                return success({}, 'invalid shot uuid', False)
            timing = Timing.objects.filter(shot=shot, \
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
        
        shot_list = Shot.objects.filter(project_id=project.id, is_disabled=False).all()
        shot_id_list = [s.id for s in shot_list]
        
        Timing.objects.filter(shot_id__in=shot_id_list, is_disabled=False).update(is_disabled=True)
        
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
        
        res_timing = Timing.objects.filter(shot=timing.shot, \
                        aux_frame_index=timing.aux_frame_index + attributes.data['distance'], shot_id=timing.shot_id, is_disabled=False).first()
        
        payload = {
            'data': TimingDto(res_timing).data if res_timing else None
        }

        return success(payload, 'timing fetched successfully', True)

# TODO: make this shifting more general depending on the usage
class ShiftTimingView(APIView):
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = ShiftTimingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        timing = Timing.objects.filter(uuid=attributes.data['timing_uuid'], is_disabled=False).first()
        if not timing:
            return success({}, 'invalid timing uuid', False)
        
        timing_list = Timing.objects.filter(shot_id=timing.shot.id, \
                                            aux_frame_index__gte=timing.aux_frame_index, is_disabled=False).order_by('aux_frame_index')
        
        timing_list.update(aux_frame_index=F('aux_frame_index') + attributes.data['shift'])

        return success({}, 'frames moved successfully', True)
    
class TimingListView(APIView):
    def __init__(self):
        self.timing_list = []
        
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = TimingListFilterDao(data=request.query_params)
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

            shot_list: Shot = Shot.objects.filter(project_id=project.id, is_disabled=False).all()
            del attributes._data['project_id']
            attributes._data['shot_id__in'] = [s.id for s in shot_list]
            
        elif 'shot_id' in attributes.data and attributes.data['shot_id']:
            shot: Shot = Shot.objects.filter(uuid=attributes.data['shot_id'], is_disabled=False).first()
            if not shot:
                return success({}, 'invalid shot uuid', False)
            
            attributes._data['shot_id'] = shot.id
        
        attributes._data['is_disabled'] = False
        
        self.timing_list = Timing.objects.filter(**attributes.data).order_by('aux_frame_index').all()

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