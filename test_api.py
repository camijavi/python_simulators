"""
Unit and integration tests for Flask API endpoints.
"""

import unittest
import json
from app import app


class TestSimulatorAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        # Will return 200 once templates/index.html is created,
        # but let's test state endpoint first
        state_res = self.client.get("/api/state")
        self.assertEqual(state_res.status_code, 200)
        data = state_res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("stack", data)
        self.assertIn("queue", data)

    def test_stack_lifecycle(self):
        # 1. Push
        res = self.client.post(
            "/api/stack/push",
            data=json.dumps({"value": "Hello"}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["operation"]["element"], "Hello")
        self.assertEqual(data["stack"]["size"], 1)

        # 2. Peek
        res = self.client.get("/api/stack/peek")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Hello")

        # 3. Pop
        res = self.client.post("/api/stack/pop")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Hello")

        # 4. Underflow Pop
        res = self.client.post("/api/stack/pop")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error_type"], "StackUnderflowError")

    def test_queue_lifecycle(self):
        # 1. Enqueue
        res = self.client.post(
            "/api/queue/enqueue",
            data=json.dumps({"value": "World"}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["operation"]["element"], "World")
        self.assertEqual(data["queue"]["size"], 1)

        # 2. Peek
        res = self.client.get("/api/queue/peek")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "World")

        # 3. Dequeue
        res = self.client.post("/api/queue/dequeue")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "World")

        # 4. Underflow Dequeue
        res = self.client.post("/api/queue/dequeue")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error_type"], "QueueUnderflowError")

    def test_bulk_fill_and_reset(self):
        res = self.client.post(
            "/api/bulk_fill",
            data=json.dumps({"target": "both", "count": 2}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["stack"]["size"], 2)
        self.assertEqual(data["queue"]["size"], 2)

        # Reset
        res = self.client.post("/api/reset")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["stack"]["size"], 0)
        self.assertEqual(data["queue"]["size"], 0)


if __name__ == "__main__":
    unittest.main()
