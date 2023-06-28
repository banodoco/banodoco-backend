from django.apps import apps
import stringcase

from authentication.v1.serializers.dto import UserDto
from user.constants import UserType

def get_model_instance(model_id, model_type):
    if model_type in UserType.value_list():     # every user will have the same model
        app_name = 'user'
        model_name = 'user'
        dto = UserDto

    instance = apps.get_model(app_name, stringcase.pascalcase(model_name)).objects.filter(uuid=model_id).first()

    return instance