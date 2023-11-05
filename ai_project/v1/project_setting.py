import datetime
from pytz import timezone
from rest_framework.views import APIView
from ai_project.models import AIModel, DBLock, InternalFileObject, Project, Setting
from ai_project.v1.serializers.dao import CreateSettingDao, LockDao, UUIDDao, UpdateSettingDao
from ai_project.v1.serializers.dto import SettingDto

from middleware.authentication import auth_required
from middleware.response import bad_request, success, unauthorized
from user.constants import UserType
from django.db import transaction

class ProjectSettingView(APIView):
    @auth_required('admin', 'user')
    def get(self, request):
        attributes = UUIDDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project_uuid = attributes.data.get('uuid')
        project = Project.objects.filter(uuid=project_uuid, is_disabled=False).first()
        if not project:
            return success({}, 'invalid project_id', False)
    
        setting = Setting.objects.filter(project_id=project.id, is_disabled=False).first()
        if not setting:
            return success({}, 'invalid project_id', False)
        
        payload = {
            'data': SettingDto(setting).data
        }

        return success(payload, 'setting fetched', True)
    
    @auth_required('admin', 'user')
    def post(self, request):
        attributes = CreateSettingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        print(attributes.data)
        
        if 'project_id' in attributes.data and attributes.data['project_id']:
            project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
            if not project:
                return success({}, 'invalid project', False)
            
            if str(project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
                return unauthorized({})
            
            attributes._data['project_id'] = project.id

        if 'default_model_id' in attributes.data and attributes.data['default_model_id']:
            model = AIModel.objects.filter(uuid=attributes.data['default_model_id'], is_disabled=False).first()
            if not model:
                return success({}, 'invalid model', False)
            
            attributes._data['default_model_id'] = model.id

        if "audio_id" in attributes.data and attributes.data["audio_id"]:
            audio = InternalFileObject.objects.filter(uuid=attributes.data["audio_id"], is_disabled=False).first()
            if not audio:
                return success({}, 'invalid audio', False)
            
            attributes._data["audio_id"] = audio.id
        
        setting = Setting.objects.create(**attributes.data)
        
        payload = {
            'data': SettingDto(setting).data
        }

        return success(payload, 'setting fetched', True)
    
    # TODO: add check on stage type while updating
    @auth_required('admin', 'user')
    def put(self, request):
        attributes = UpdateSettingDao(data=request.data)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        project: Project = Project.objects.filter(uuid=attributes.data['project_id'], is_disabled=False).first()
        if not project:
            return success({}, 'invalid project', False)
        
        if str(project.user.uuid).replace('-','') != request.role_id and request.role_type != UserType.ADMIN.value:
            return unauthorized({})
        
        print(attributes.data)
        attributes._data['project_id'] = project.id
        
        setting = Setting.objects.filter(project_id=project.id, is_disabled=False).first()
        if not setting:
            return success({}, 'invalid project', False)

        if 'default_model_id' in attributes.data and attributes.data['default_model_id']:
            model = AIModel.objects.filter(uuid=attributes.data['default_model_id'], is_disabled=False).first()
            if not model:
                return success({}, 'invalid model', False)
            
            attributes._data['default_model_id'] = model.id

        if "audio_id" in attributes.data and attributes.data["audio_id"]:
            audio = InternalFileObject.objects.filter(uuid=attributes.data["audio_id"], is_disabled=False).first()
            if not audio:
                return success({}, 'invalid audio', False)
            
            attributes._data["audio_id"] = audio.id

        if 'model_id' in attributes.data and attributes.data['model_id']:
            model = AIModel.objects.filter(uuid=attributes.data['model_id'], is_disabled=False).first()
            if not model:
                return success({}, 'invalid model', False)
            
            attributes._data['model_id'] = model.id
        
        for attr, value in attributes.data.items():
            setattr(setting, attr, value)
        setting.save()
        
        payload = {
            'data': SettingDto(setting).data
        }

        return success(payload, 'setting fetched', True)
    

class LockAPIView(APIView):
    # TODO: think of a proper auth to apply here
    def get(self, request):
        attributes = LockDao(data=request.query_params)
        if not attributes.is_valid():
            return bad_request(attributes.errors)
        
        with transaction.atomic():
            if attributes.data['action'] == 'acquire':
                lock, created = DBLock.objects.get_or_create(row_key=attributes.data['key'])
                if lock.created_on + datetime.timedelta(minutes=1) < datetime.datetime.now(tz=timezone('UTC')):
                    created = True
                    
                payload = {
                    'data': True if created else False
                }
                return success(payload, 'success', True)
            else:
                DBLock.objects.filter(row_key=attributes.data['key']).delete()
                return success({'data': True}, 'success', True)
        