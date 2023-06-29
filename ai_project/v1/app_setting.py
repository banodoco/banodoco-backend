from rest_framework.views import APIView
from ai_project.models import AppSetting
from ai_project.v1.serializers.dao import CreateAppSettingDao, UUIDDao, UpdateAppSettingDao
from ai_project.v1.serializers.dto import AppSettingDto

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType
from user.models import User

class AppSettingView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        app_setting = AppSetting.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not app_setting:
            return bad_request('App setting not found')

        payload = {
            'data': AppSettingDto(app_setting).data
        }

        return success(payload, 'successfully fetched app setting', True)
    
    @auth_required('admin', 'user')
    def put(self, request):
        attributes = UpdateAppSettingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        print(attributes.data)
        
        if 'uuid' in attributes.data and attributes.data['uuid']:
            app_setting = AppSetting.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
            if app_setting.user.uuid != request.role_id and request.role_type != UserType.ADMIN.value:
                return unauthorized({})
        else:
            cur_user = User.objects.filter(uuid=request.role_id, is_disabled=False).first()
            if not cur_user:
                return unauthorized({})
            
            app_setting = AppSetting.objects.filter(uuid=cur_user.uuid, is_disabled=False).first()

        if 'user_id' in attributes.data and attributes.data['user_id']:
            if request.role_id != attributes.data['user_id'] and request.role_type != UserType.ADMIN.value:
                return unauthorized({})
            
            user = User.objects.filter(uuid=attributes.data['user_id'], is_disabled=False).first()
            if not user:
                return success({}, 'invalid user', False)
            
            print(attributes.data)
            attributes._data['user_id'] = user.id

        for attr, value in attributes.data.items():
            setattr(app_setting, attr, value)
        app_setting.save()

        return success({}, 'app_setting updated successfully', True)
    
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = CreateAppSettingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        print(attributes.data)
        
        user_id = attributes.data['user_id'] if 'user_id' in attributes.data and \
            attributes.data['user_id'] and request.role_type == UserType.ADMIN.value else request.role_id
        if user_id:
            user = User.objects.filter(uuid=user_id, is_disabled=False).first()
            if not user:
                return success({}, 'invalid user', False)
            
            attributes._data['user_id'] = user.id
        
        app_setting = AppSetting.objects.create(**attributes.data)
        
        payload = {
            'data': AppSettingDto(app_setting).data
        }
        
        return success(payload, 'app_setting created successfully', True)
    
    @auth_required('admin', 'user')
    def delete(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)

        app_setting = AppSetting.objects.filter(uuid=attributes.data['uuid'], is_disabled=False).first()
        if not app_setting:
            return bad_request('App setting not found')

        if app_setting.user.uuid != request.role_id and request.role_type != UserType.ADMIN.value:
            return unauthorized({})
        
        app_setting.is_disabled = True
        app_setting.save()

        return success({}, 'app_setting deleted successfully', True)

# TODO: figure out how app secrets will work in the hosted version
# TODO: figure how to store the encryption secret key
class AppSecretView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        user_uuid = request.role_id
        if user_uuid:
            user: User = User.objects.filter(uuid=user_uuid, is_disabled=False).first()
            if not user:
                return success({}, 'invalid user', False)
            
            app_setting = AppSetting.objects.filter(user_id=user.id, is_disabled=False).first()
        else:
            app_setting = AppSetting.objects.filter(is_disabled=False).first()
        
        payload = {
            'data': {
                'aws_access_key': app_setting.aws_access_key_decrypted,
                'aws_secret_key': app_setting.aws_secret_access_key_decrypted,
                'replicate_key': app_setting.replicate_key_decrypted,
                'replicate_username': app_setting.replicate_username
            }
        }

        return success(payload, 'app_setting fetched successfully', True)

        