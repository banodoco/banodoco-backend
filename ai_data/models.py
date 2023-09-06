import json
from banodoco.base_model import BaseModel
from django.db import models


class TrainingData(BaseModel):
    author_id = models.CharField(max_length=255, default="", blank=True, null=True)
    video_url = models.TextField(default="", blank=True, null=True, db_index=True)
    caption_list = models.TextField(default="", blank=True)
    total_caption_count = models.IntegerField(default=0)
    rating_list = models.TextField(default="", blank=True)
    total_rating_count = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)

    class Meta:
        db_table = 'training_data'
    
    def add_caption(self, caption):
        cur_list = json.loads(self.caption_list) if self.caption_list else []
        cur_list.append(caption)
        self.caption_list = json.dumps(cur_list)
        self.total_caption_count += 1

    def add_rating(self, rating):
        cur_list = json.loads(self.rating_list) if self.rating_list else []
        cur_list.append(rating)
        total_sum = sum(cur_list)
        self.rating_list = json.dumps(cur_list)
        self.total_rating_count += 1
        self.avg_rating = round(total_sum / self.total_rating_count, 2)