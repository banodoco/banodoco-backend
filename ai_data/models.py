import json
from ai_data.utils import ClipData, VideoDataManager
from banodoco.base_model import BaseModel
from django.db import models


'''
user_data format (encoded string)
user_data = {obj1, obj2..}
where
obj = "{start_index}--{end_index}": {
    "version": 1,   # maintains the version of data structure
    "caption_list": ["test1", "test2"],
    "caption_count": 2,
    "rating_list": [1,0,-1,1],
    "rating_count": 4,
    "avg_rating": 0.2
}
'''
class TrainingData(BaseModel):
    author_id = models.CharField(max_length=255, default="", blank=True, null=True)
    video_url = models.TextField(default="", blank=True, null=True, db_index=True)
    user_data = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'training_data'
    
    def add_caption(self, start_idx, end_idx, caption):
        clip_data: ClipData = VideoDataManager.get_clip_data(start_idx, end_idx, self.user_data, create_new=True)

        cur_list = clip_data.caption_list if clip_data.caption_list else []
        cur_list.append(caption)
        clip_data.caption_list = cur_list
        clip_data.caption_count += 1

        self.user_data = VideoDataManager.update_clip_data(start_idx, end_idx, self.user_data, clip_data)

    def add_rating(self, start_idx, end_idx, rating):
        clip_data: ClipData = VideoDataManager.get_clip_data(start_idx, end_idx, self.user_data, create_new=True)

        cur_list = clip_data.rating_list if clip_data.rating_list else []
        cur_list.append(rating)
        total_sum = sum(cur_list)
        clip_data.rating_list = cur_list
        clip_data.rating_count += 1
        clip_data.avg_rating = round(total_sum / clip_data.rating_count, 2)

        self.user_data = VideoDataManager.update_clip_data(start_idx, end_idx, self.user_data, clip_data)