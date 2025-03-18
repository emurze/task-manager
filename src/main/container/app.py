from modules.tasks.application import tasks_module
from modules.tasks.infra.repositories import TaskSQLAlchemyRepository
from seedwork.application.application import Application
from seedwork.application.providers import Provider
from seedwork.application.uows import SqlAlchemyUnitOfWork
from seedwork.config import Config
from seedwork.infra.db import get_db_adapter


def create_application(config: Config) -> Application:
    db_adapter = get_db_adapter(config)
    session_factory = db_adapter.session_factory
    app = Application(
        dependencies={
            "config": config,
            "session_factory": session_factory,
            "uow": Provider(
                SqlAlchemyUnitOfWork,
                session_factory,
                {
                    "tasks": TaskSQLAlchemyRepository,
                },
            ),
        },
    )
    app["app"] = app
    app.include_submodule(tasks_module)
    return app
