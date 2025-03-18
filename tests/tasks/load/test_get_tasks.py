from locust import HttpUser, task, between


class BaseTaskUser(HttpUser):
    wait_time = between(1, 3)
    task_id = None
    abstract = True

    def on_start(self):
        """Создаём тестовую задачу перед началом тестов."""
        response = self.client.post("/tasks", json={"name": "Test Task"})
        if response.status_code == 201:
            self.task_id = response.json()
        else:
            self.task_id = None

    def on_stop(self):
        """Удаляем задачу по завершении теста (если она осталась)."""
        if self.task_id:
            self.client.delete(f"/tasks/{self.task_id}")


class GetTasksUser(BaseTaskUser):
    @task(3)
    def get_tasks(self):
        """Получение списка задач."""
        self.client.get("/tasks")
