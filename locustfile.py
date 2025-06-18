from locust import HttpUser, task, between
from uuid import uuid4
from itertools import cycle

video_urls = cycle(f"http://s1.origin-cluster/video/1488/{uuid4().hex}.m3u8" for _ in range(1000))


class BalancerUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(4)
    def test_balance_request(self):
        with self.client.get(
            "/",
            params={"video": next(video_urls)},
            catch_response=True,
            allow_redirects=False,
        ) as resp:
            if resp.status_code == 301:
                resp.success()
            else:
                resp.failure(f"Expected 301, got {resp.status_code}")

    @task(2)
    def test_invalid_video(self):
        with self.client.get("/", params={"video": "not_a_url"}, catch_response=True) as resp:
            if resp.status_code == 422:
                resp.success()
            else:
                resp.failure(f"Expected 422, got {resp.status_code}")

    @task(1)
    def test_no_video_param(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code == 422:
                resp.success()
            else:
                resp.failure(f"Expected 422, got {resp.status_code}")
