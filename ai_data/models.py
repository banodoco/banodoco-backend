import json
from ai_data.utils import ClipData, VideoDataManager
from banodoco.base_model import BaseModel
from django.db import models


'''
user_data format (encoded string)
user_data = {obj1, obj2..}
where
obj = "{start_index}--{end_index}": {
    "caption_count": 1,
    "rating_count": 1,
    "avg_rating": 3,
    "user_data_list": [
        {
            "user_id": "abc123",
            "caption": "test1",
            "rating": 3
        }
    ],
}
'''
class TrainingData(BaseModel):
    video_url = models.TextField(default="", blank=True, null=True, db_index=True)
    user_data = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'training_data'
    
    def add_caption(self, start_idx, end_idx, user_id, caption):
        clip_data: ClipData = VideoDataManager.get_clip_data(start_idx, end_idx, self.user_data, create_new=True)

        user_found = False
        for ud in clip_data.user_data_list:
            if ud['user_id'] == user_id:
                user_found = True
                if ud['caption'] == '':
                    clip_data.caption_count += 1
                ud['caption'] = caption
                break

        if not user_found:
            clip_data.user_data_list.append({
                "user_id": user_id,
                "rating": "",
                "caption": caption
            })
            clip_data.caption_count += 1
        
        self.user_data = VideoDataManager.update_clip_data(start_idx, end_idx, self.user_data, clip_data)

    def add_rating(self, start_idx, end_idx, user_id, rating):
        clip_data: ClipData = VideoDataManager.get_clip_data(start_idx, end_idx, self.user_data, create_new=True)

        user_found = False
        for ud in clip_data.user_data_list:
            if ud['user_id'] == user_id:
                user_found = True

                if ud['rating'] == '':
                    prev_rating = 0
                    clip_data.rating_count += 1
                else:
                    prev_rating = ud['rating']

                clip_data.avg_rating += round((rating - (ud['rating'] if ud['rating'] else 0))/clip_data.rating_count)
                ud['rating'] = rating
                break

        if not user_found:
            clip_data.user_data_list.append({
                "user_id": user_id,
                "rating": rating,
                "caption": ""
            })
            clip_data.rating_count += 1
            clip_data.avg_rating += round(rating/clip_data.rating_count)
        
        self.user_data = VideoDataManager.update_clip_data(start_idx, end_idx, self.user_data, clip_data)


'''
user_rating format : [
    {
        "user_id": "abc123",
        "rating": 2
    }
]
'''
class ImageCaptionData(BaseModel):
    img_1_url = models.TextField(default="", blank=True)
    img_1_desc = models.TextField(default="", blank=True)
    img_2_url = models.TextField(default="", blank=True)
    img_2_desc = models.TextField(default="", blank=True)
    instruction = models.TextField(default="", blank=True)
    user_rating = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'image_caption_data'

    @property
    def user_rating_list(self):
        return json.loads(self.user_rating) if self.user_rating else []
    
    def update_user_rating(self, user_id, val):
        if user_id:
            rating_list = self.user_rating_list
            user_found = False
            for r in rating_list:
                if r['user_id'] == user_id:
                    user_found = True
                    r['rating'] = val
            
            if not user_found:
                rating_list.append({
                    "user_id": user_id,
                    "rating": val
                })

            self.user_rating = json.dumps(rating_list)