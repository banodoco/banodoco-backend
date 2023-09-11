import json
from rest_framework.views import APIView
from ai_data.models import ImageCaptionData
from ai_data.v1.serializers.dao import CaptionDataListFilterDao, CreateImageCaptionDataDao, UUIDDao, UpdateImageCaptionDataDao
from ai_data.v1.serializers.dto import ImageCaptionDataDto, ImageCaptionDataListItemDto
from middleware.authentication import static_auth_required
from django.core.paginator import Paginator

from middleware.response import bad_request, success

class ImageCaptionCRUDView(APIView):
    @static_auth_required
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        caption_data = ImageCaptionData.objects.filter(uuid=attributes.data['uuid'],\
                                                        is_disabled=False).first()
        if not caption_data:
            return success({}, "invalid uuid", False)
        
        payload = {
            'data':  ImageCaptionDataDto(caption_data).data
        }

        return success(payload, 'data fetched successfully', True)
    
    @static_auth_required
    def post(self, request):
        attributes = CreateImageCaptionDataDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        #NOTE: right now creating object without any duplicate check
        caption_data = ImageCaptionData.objects.create(**attributes.data)

        payload = {
            'data': ImageCaptionDataDto(caption_data).data
        }

        return success(payload, 'data created successfully', True)
    
    @static_auth_required
    def put(self, request):
        attributes = UpdateImageCaptionDataDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        caption_data = ImageCaptionData.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not caption_data:
            return success({}, "invalid uuid", False)
        
        #NOTE: right now just adding any incoming rating to the list
        if 'user_rating' in attributes.data:
            caption_data_rating_list = caption_data.user_rating_list
            caption_data_rating_list.append(attributes.data['user_rating'])
            print(attributes.data)
            attributes._data['user_rating'] = json.dumps(caption_data_rating_list)

        for attr, value in attributes.data.items():
            setattr(caption_data, attr, value)
        caption_data.save()

        payload = {
            'data': ImageCaptionDataDto(caption_data).data
        }

        return success(payload, 'data updated successfully', True)
    
    @static_auth_required
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        caption_data = ImageCaptionData.objects.filter(uuid=attributes.data['uuid'],\
                                                        is_disabled=False).first()
        if caption_data:
            caption_data.is_disabled = True
            caption_data.save()

        return success({}, "caption data deleted successfully", True)
    

class ImageCaptionListView(APIView):
    def __init__(self):
        self.caption_data_list = []

    @static_auth_required
    def get(self, request):
        attributes = CaptionDataListFilterDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        page = attributes.data['page']
        del attributes._data['page']
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]

        attributes._data['is_disabled'] = False
        
        self.caption_data_list = ImageCaptionData.objects.filter(**attributes.data).all()

        paginator = Paginator(self.caption_data_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": ImageCaptionDataListItemDto(
                paginator.page(page), many=True
            ).data,
        }
        return success(payload, "training data list fetched successfully", True)
