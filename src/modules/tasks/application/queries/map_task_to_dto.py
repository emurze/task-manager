from modules.tasks.infra.repositories import TaskModel


def map_task_to_dto(task: TaskModel) -> dict:
    return {"id": task.id, "name": task.name}
