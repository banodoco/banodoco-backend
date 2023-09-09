from dataclasses import dataclass
import json
from typing import List


@dataclass
class ClipData:
    caption_list: List[str]
    caption_count: int
    rating_list: List[int]
    rating_count: int
    avg_rating: float

    def to_json(self):
        return {
            "caption_list": self.caption_list,
            "caption_count": self.caption_count,
            "rating_list": self.rating_list,
            "rating_count": self.rating_count,
            "avg_rating": self.avg_rating
        }


class VideoDataManager:
    @staticmethod
    def get_clip_data(start_idx, end_idx, user_data, create_new=False):
        if user_data:
            user_data = json.loads(user_data)
            for k,v in user_data.items():
                if k == f"{start_idx}--{end_idx}":
                    return ClipData(**v)
        
        if create_new:
            return VideoDataManager.create_clip_data(start_idx, end_idx)
        

    @staticmethod
    def update_clip_data(start_idx, end_idx, user_data, clip_data: ClipData):
        user_data = json.loads(user_data) if user_data else {}
        user_data[f"{start_idx}--{end_idx}"] = clip_data.to_json()
        return json.dumps(user_data) if user_data else None


    @staticmethod
    def create_clip_data(start_idx, end_idx):
        # creates a clip data with default values
        clip_data = {
            "caption_list": [],
            "caption_count": 0,
            "rating_list": [],
            "rating_count": 0,
            "avg_rating": 0
        }

        return ClipData(**clip_data)