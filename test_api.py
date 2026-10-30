"""
Unit and integration tests for Flask API endpoints, including
Stack, Queue, and Sorted Linked List.
"""

import unittest
import json
from app import app


class TestSimulatorAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_state_and_index(self):
        index_res = self.client.get("/")
        self.assertEqual(index_res.status_code, 200)
        self.assertIn("Simulador Visual de Estructuras de Datos".encode("utf-8"), index_res.data)
        self.assertIn("LIFO".encode("utf-8"), index_res.data)
        self.assertIn("FIFO".encode("utf-8"), index_res.data)
        self.assertIn("Lista Enlazada".encode("utf-8"), index_res.data)

        state_res = self.client.get("/api/state")
        self.assertEqual(state_res.status_code, 200)
        data = state_res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("stack", data)
        self.assertIn("queue", data)
        self.assertIn("linked_list", data)

    def test_stack_lifecycle(self):
        # 1. Push
        res = self.client.post(
            "/api/stack/push",
            data=json.dumps({"value": "Plato 1"}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["operation"]["element"], "Plato 1")
        self.assertEqual(data["stack"]["size"], 1)

        # 2. Peek
        res = self.client.get("/api/stack/peek")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Plato 1")

        # 3. Pop
        res = self.client.post("/api/stack/pop")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Plato 1")

        # 4. Underflow Pop
        res = self.client.post("/api/stack/pop")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error_type"], "StackUnderflowError")

    def test_queue_lifecycle(self):
        # 1. Enqueue
        res = self.client.post(
            "/api/queue/enqueue",
            data=json.dumps({"value": "Turno 1"}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["operation"]["element"], "Turno 1")
        self.assertEqual(data["queue"]["size"], 1)

        # 2. Peek
        res = self.client.get("/api/queue/peek")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Turno 1")

        # 3. Dequeue
        res = self.client.post("/api/queue/dequeue")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["operation"]["element"], "Turno 1")

        # 4. Underflow Dequeue
        res = self.client.post("/api/queue/dequeue")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error_type"], "QueueUnderflowError")

    def test_linked_list_lifecycle(self):
        # 1. Insert 30, then 10, then 20 (should be sorted 10, 20, 30)
        for val in [30, 10, 20]:
            res = self.client.post(
                "/api/linked_list/insert",
                data=json.dumps({"value": val}),
                content_type="application/json"
            )
            self.assertEqual(res.status_code, 200)

        state = self.client.get("/api/state").get_json()["linked_list"]
        self.assertEqual(state["items"], [10, 20, 30])
        self.assertEqual(state["head"], 10)
        self.assertEqual(state["tail"], 30)

        # 2. Attempt duplicate insert (rejected per read.me)
        dup_res = self.client.post(
            "/api/linked_list/insert",
            data=json.dumps({"value": 20}),
            content_type="application/json"
        )
        self.assertEqual(dup_res.status_code, 400)
        self.assertEqual(dup_res.get_json()["error_type"], "DuplicateValueError")

        # 3. Search
        search_res = self.client.post(
            "/api/linked_list/search",
            data=json.dumps({"value": 20}),
            content_type="application/json"
        )
        self.assertEqual(search_res.status_code, 200)
        self.assertEqual(search_res.get_json()["operation"]["index"], 1)

        # 4. Remove specific value (20)
        rem_res = self.client.post(
            "/api/linked_list/remove_value",
            data=json.dumps({"value": 20}),
            content_type="application/json"
        )
        self.assertEqual(rem_res.status_code, 200)
        self.assertEqual(rem_res.get_json()["linked_list"]["items"], [10, 30])

        # 5. Remove head (10)
        rem_head = self.client.post("/api/linked_list/remove_head")
        self.assertEqual(rem_head.status_code, 200)
        self.assertEqual(rem_head.get_json()["linked_list"]["items"], [30])

        # 6. Remove tail (30)
        rem_tail = self.client.post("/api/linked_list/remove_tail")
        self.assertEqual(rem_tail.status_code, 200)
        self.assertEqual(rem_tail.get_json()["linked_list"]["items"], [])

    def test_bulk_fill_and_reset(self):
        res = self.client.post(
            "/api/bulk_fill",
            data=json.dumps({"target": "all", "count": 2}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["stack"]["size"], 2)
        self.assertEqual(data["queue"]["size"], 2)
        self.assertGreaterEqual(data["linked_list"]["size"], 1)

        # Reset
        res = self.client.post("/api/reset")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["stack"]["size"], 0)
        self.assertEqual(data["queue"]["size"], 0)
        self.assertEqual(data["linked_list"]["size"], 0)


if __name__ == "__main__":
    unittest.main()
