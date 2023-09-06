from rest_framework.views import APIView
from ai_data.models import TrainingData
from ai_data.v1.serializers.dao import TrainingDataDao, TrainingDataFilterDao, UpdateTrainingDataDao
from ai_data.v1.serializers.dto import TrainingDataDto, TrainingDataListItemDto
from django.core.paginator import Paginator

from middleware.authentication import static_auth_required
from middleware.response import bad_request, success

class TrainingDataCRUDView(APIView):
    def _get_training_data(self, data):
        if 'uuid' in data:
            ai_data = TrainingData.objects.filter(uuid=data['uuid'], is_disabled=False).first()
        elif 'video_url' in data:
            ai_data = TrainingData.objects.filter(video_url=data['video_url'], is_disabled=False).first()

        return ai_data

    @static_auth_required
    def get(self, request):
        attributes = TrainingDataDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        ai_data = self._get_training_data(attributes.data)

        if not ai_data:
            return success({}, "invalid uuid or video_url", False)
        
        payload = {
            'data':  TrainingDataDto(ai_data)
        }

        return success(payload, 'data fetched successfully', True)

    @static_auth_required
    def put(self, request):
        attributes = UpdateTrainingDataDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        ai_data = self._get_training_data(attributes.data)

        if not ai_data:
            return success({}, "invalid uuid or video_url", False)

        if 'caption' in attributes.data and attributes.data['caption']:
            ai_data.add_caption(attributes.data['caption'])
        
        if 'rating' in attributes.data and attributes.data['rating'] != None:
            ai_data.add_rating(attributes.data['rating'])

        ai_data.save()

        payload = {
            'data': TrainingDataDto(ai_data)
        }

        return success(payload, 'data updated successfully', True)

    @static_auth_required
    def delete(self, request):
        attributes = TrainingDataDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        ai_data = self._get_training_data(attributes.data)
        if ai_data:
            ai_data.is_disabled = False
            ai_data.save()

        return success({}, 'data cleared', True)

class TrainingDataListView(APIView):
    def __init__(self):
        self.training_data_list = []

    @static_auth_required
    def get(self, request):
        attributes = TrainingDataFilterDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        page = attributes.data['page']
        del attributes._data['page']
        self.data_per_page = attributes.data["data_per_page"]
        del attributes._data["data_per_page"]
        
        if 'min_avg_rating' in attributes.data:
            v = attributes.data['min_avg_rating']
            del attributes._data['min_avg_rating']
            attributes._data['avg_rating__gte'] = v

        attributes._data['is_disabled'] = False
        
        self.training_data_list = TrainingData.objects.filter(**attributes.data).all()

        paginator = Paginator(self.training_data_list, self.data_per_page)
        if page > paginator.num_pages or page < 1:
            return success({}, "invalid page number", False)
        
        payload = {
            "data_per_page": self.data_per_page,
            "page": page,
            "total_pages": paginator.num_pages,
            "count": paginator.count,
            "data": TrainingDataListItemDto(
                paginator.page(page), many=True
            ).data,
        }
        return success(payload, "training data list fetched successfully", True)