from util.extended_enum import ExtendedEnum


class ServerType(ExtendedEnum):
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'

class InternalResponse:
    def __init__(self, data, message, status):
        self.status = status
        self.message = message
        self.data = data

class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

class AIModelType(ExtendedEnum):
    LORA = 'LoRA'
    DREAMBOOTH = 'Dreambooth'
    BASE_SD = 'Base_SD'
    CONTROLNET = 'controlnet'
    STYLEGAN_NADA = "StyleGAN-NADA"
    PIX_2_PIX = 'pix2pix'

class GuidanceType(ExtendedEnum):
    DRAWING = 'drawing'
    IMAGE = 'image'

class InternalFileType(ExtendedEnum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    GIF = 'gif'

# Internal file tags
class InternalFileTag(ExtendedEnum):
    BACKGROUND_IMAGE = 'background_image'
    GENERATED_VIDEO = 'generated_video'
    COMPLETE_GENERATED_VIDEO = 'complete_generated_video'
    INPUT_VIDEO = 'input_video'
    TEMP_IMAGE = 'temp'
    GALLERY_IMAGE = 'gallery_image'
    SHORTLISTED_GALLERY_IMAGE = 'shortlisted_gallery_image'
    TEMP_GALLERY_IMAGE = 'temp_gallery_image'

class InferenceParamType(ExtendedEnum):
    REPLICATE_INFERENCE = "replicate_inference"     # replicate url for queue inference and other data
    QUERY_DICT = "query_dict"                       # query dict of standardized inference params
    ORIGIN_DATA = "origin_data"                     # origin data - used to store file once inference is completed

class InferenceStatus(ExtendedEnum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class AnimationStyleType(ExtendedEnum):
    INTERPOLATION = "Interpolation"
    DIRECT_MORPHING = "Direct Morphing"

class SortOrder(ExtendedEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"

class InferenceType(ExtendedEnum):
    FRAME_TIMING_IMAGE_INFERENCE = "frame_timing_inference"         # for generating variants of a frame
    FRAME_TIMING_VIDEO_INFERENCE = "frame_timing_video_inference"   # for generating variants of a video
    FRAME_INTERPOLATION = "frame_interpolation"                     # for generating single/multiple interpolated videos
    GALLERY_IMAGE_GENERATION = "gallery_image_generation"           # for generating gallery images
    FRAME_INPAINTING = "frame_inpainting"                           # for generating inpainted frames

class ProjectMetaData(ExtendedEnum):
    DATA_UPDATE = "data_update"                     # info regarding cache/data update when runner updates the db
    GALLERY_UPDATE = "gallery_update"
    BACKGROUND_IMG_LIST = "background_img_list"
    SHOT_VIDEO_UPDATE = "shot_video_update"

replicate_status_map = {
    "starting": InferenceStatus.QUEUED.value,
    "processing": InferenceStatus.IN_PROGRESS.value,
    "succeeded": InferenceStatus.COMPLETED.value,
    "failed": InferenceStatus.FAILED.value,
    "canceled": InferenceStatus.CANCELED.value
}

S3_FOLDER_PATH = {
    'misc': 'misc/',
    'general_pics': 'general_pics/',
    'general_videos': 'general_videos/'
}