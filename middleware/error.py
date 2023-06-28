import os
import traceback

from dotenv import load_dotenv

from middleware.response import error
import sentry_sdk
from sentry_sdk import configure_scope

load_dotenv()
SERVER = os.getenv('SERVER', 'development')

class SentryMiddleware(object):
    def process_exception(self, request, exception):
        self.log(request, traceback)

        if SERVER == 'production':
            return error({})
        return error(str(exception))

    def log(self, request, traceback):
        if SERVER == 'development':
            print(traceback.print_exc())
            return

        with configure_scope() as scope:
            scope.set_extra('request_body', str(request.body))
            scope.set_extra('request_type', request.META['REQUEST_METHOD'])
            scope.set_extra('path', request.get_full_path())
            scope.set_extra('server', request.META['SERVER_NAME'])
            scope.set_extra('port', request.META['SERVER_PORT'])

            scope.set_tag('environment', SERVER)
            for key, value in request.META.items():
                scope.set_tag(key, value)

            sentry_sdk.capture_exception()
