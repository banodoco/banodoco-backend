import sentry_sdk


def log_sentry_exception(tag, request, response):
    with sentry_sdk.configure_scope() as scope:
        scope.set_extra("request", request)
        scope.set_extra("response", response)
    sentry_sdk.capture_exception(Exception(tag))