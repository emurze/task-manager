from starlette.requests import Request

from seedwork.application.application import Application


def get_application(request: Request) -> Application:
    return request.app.extra["application"]
