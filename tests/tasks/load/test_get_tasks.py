from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    host = "http://0.0.0.0:80"

    @task
    def hello_world(self):
        self.client.get("/tasks")
