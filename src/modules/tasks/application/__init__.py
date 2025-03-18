import importlib

from seedwork.application.application_module import ApplicationModule

tasks_module = ApplicationModule("tasks")
importlib.import_module("modules.tasks.application.commands")
importlib.import_module("modules.tasks.application.queries")
