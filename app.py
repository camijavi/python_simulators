"""
Flask Application for Stack and Queue Visual Simulator.
Provides RESTful APIs for Stack (LIFO) and Queue (FIFO) data structures,
and serves a reactive, interactive frontend.
"""

import os
import uuid
import random
from flask import Flask, render_template, request, jsonify, session
from structures import (
    Stack,
    Queue,
    StackOverflowError,
    StackUnderflowError,
    QueueOverflowError,
    QueueUnderflowError,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-simulators-2026")

# In-memory store for session-based simulators
# Structure: {session_id: {"stack": Stack(), "queue": Queue()}}
SIMULATOR_STORE = {}

SAMPLE_VALUES = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry",
    "Fig", "Grape", "Honeydew", "Kiwi", "Lemon",
    "Mango", "Nectarine", "Orange", "Peach", "Plum"
]


def get_simulator():
    """Retrieve or initialize the Stack and Queue for the current session."""
    if "session_id" not in session or session["session_id"] not in SIMULATOR_STORE:
        session["session_id"] = str(uuid.uuid4())
        SIMULATOR_STORE[session["session_id"]] = {
            "stack": Stack(capacity=7),
            "queue": Queue(capacity=7),
        }
    return SIMULATOR_STORE[session["session_id"]]


@app.route("/")
def index():
    """Serve the main simulator visual interface."""
    # Ensure session is initialized
    get_simulator()
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    """Return the current serialized state of both Stack and Queue."""
    sim = get_simulator()
    return jsonify({
        "success": True,
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
        "stack_history": sim["stack"].history[-10:],
        "queue_history": sim["queue"].history[-10:],
    })


# ==========================================
# Stack Endpoints (LIFO)
# ==========================================

@app.route("/api/stack/push", methods=["POST"])
def stack_push():
    """Push an item onto the stack."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    val = data.get("value")

    if val is None or str(val).strip() == "":
        val = random.choice(SAMPLE_VALUES)
    else:
        val = str(val).strip()

    try:
        record = sim["stack"].push(val)
        return jsonify({
            "success": True,
            "operation": record,
            "stack": sim["stack"].to_dict(),
            "message": record["message"]
        })
    except StackOverflowError as e:
        return jsonify({
            "success": False,
            "error_type": "StackOverflowError",
            "message": str(e),
            "stack": sim["stack"].to_dict()
        }), 400


@app.route("/api/stack/pop", methods=["POST"])
def stack_pop():
    """Pop the top item from the stack."""
    sim = get_simulator()
    try:
        record = sim["stack"].pop()
        return jsonify({
            "success": True,
            "operation": record,
            "stack": sim["stack"].to_dict(),
            "message": record["message"]
        })
    except StackUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "StackUnderflowError",
            "message": str(e),
            "stack": sim["stack"].to_dict()
        }), 400


@app.route("/api/stack/peek", methods=["GET"])
def stack_peek():
    """Peek at the top item without removing it."""
    sim = get_simulator()
    try:
        record = sim["stack"].peek()
        return jsonify({
            "success": True,
            "operation": record,
            "stack": sim["stack"].to_dict(),
            "message": record["message"]
        })
    except StackUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "StackUnderflowError",
            "message": str(e),
            "stack": sim["stack"].to_dict()
        }), 400


@app.route("/api/stack/clear", methods=["POST"])
def stack_clear():
    """Clear all items from the stack."""
    sim = get_simulator()
    record = sim["stack"].clear()
    return jsonify({
        "success": True,
        "operation": record,
        "stack": sim["stack"].to_dict(),
        "message": record["message"]
    })


@app.route("/api/stack/capacity", methods=["POST"])
def stack_capacity():
    """Update stack capacity."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    try:
        new_cap = int(data.get("capacity", 7))
        sim["stack"].set_capacity(new_cap)
        return jsonify({
            "success": True,
            "capacity": sim["stack"].capacity,
            "stack": sim["stack"].to_dict(),
            "message": f"Stack capacity set to {new_cap}."
        })
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ==========================================
# Queue Endpoints (FIFO)
# ==========================================

@app.route("/api/queue/enqueue", methods=["POST"])
def queue_enqueue():
    """Enqueue an item at the rear of the queue."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    val = data.get("value")

    if val is None or str(val).strip() == "":
        val = random.choice(SAMPLE_VALUES)
    else:
        val = str(val).strip()

    try:
        record = sim["queue"].enqueue(val)
        return jsonify({
            "success": True,
            "operation": record,
            "queue": sim["queue"].to_dict(),
            "message": record["message"]
        })
    except QueueOverflowError as e:
        return jsonify({
            "success": False,
            "error_type": "QueueOverflowError",
            "message": str(e),
            "queue": sim["queue"].to_dict()
        }), 400


@app.route("/api/queue/dequeue", methods=["POST"])
def queue_dequeue():
    """Dequeue an item from the front of the queue."""
    sim = get_simulator()
    try:
        record = sim["queue"].dequeue()
        return jsonify({
            "success": True,
            "operation": record,
            "queue": sim["queue"].to_dict(),
            "message": record["message"]
        })
    except QueueUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "QueueUnderflowError",
            "message": str(e),
            "queue": sim["queue"].to_dict()
        }), 400


@app.route("/api/queue/peek", methods=["GET"])
def queue_peek():
    """Peek at the front item without removing it."""
    sim = get_simulator()
    try:
        record = sim["queue"].peek()
        return jsonify({
            "success": True,
            "operation": record,
            "queue": sim["queue"].to_dict(),
            "message": record["message"]
        })
    except QueueUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "QueueUnderflowError",
            "message": str(e),
            "queue": sim["queue"].to_dict()
        }), 400


@app.route("/api/queue/clear", methods=["POST"])
def queue_clear():
    """Clear all items from the queue."""
    sim = get_simulator()
    record = sim["queue"].clear()
    return jsonify({
        "success": True,
        "operation": record,
        "queue": sim["queue"].to_dict(),
        "message": record["message"]
    })


@app.route("/api/queue/capacity", methods=["POST"])
def queue_capacity():
    """Update queue capacity."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    try:
        new_cap = int(data.get("capacity", 7))
        sim["queue"].set_capacity(new_cap)
        return jsonify({
            "success": True,
            "capacity": sim["queue"].capacity,
            "queue": sim["queue"].to_dict(),
            "message": f"Queue capacity set to {new_cap}."
        })
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ==========================================
# Bulk & Reset Utilities
# ==========================================

@app.route("/api/reset", methods=["POST"])
def reset_all():
    """Reset both stack and queue to empty state."""
    sim = get_simulator()
    sim["stack"].clear()
    sim["queue"].clear()
    sim["stack"].history.clear()
    sim["queue"].history.clear()
    return jsonify({
        "success": True,
        "message": "Both stack and queue have been reset.",
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
    })


@app.route("/api/bulk_fill", methods=["POST"])
def bulk_fill():
    """Fill either stack or queue with 3 random values."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    target = data.get("target", "both")  # "stack", "queue", or "both"
    count = min(int(data.get("count", 3)), 5)
    added = {"stack": [], "queue": []}

    if target in ("stack", "both"):
        for _ in range(count):
            if not sim["stack"].is_full():
                val = random.choice(SAMPLE_VALUES)
                sim["stack"].push(val)
                added["stack"].append(val)

    if target in ("queue", "both"):
        for _ in range(count):
            if not sim["queue"].is_full():
                val = random.choice(SAMPLE_VALUES)
                sim["queue"].enqueue(val)
                added["queue"].append(val)

    return jsonify({
        "success": True,
        "added": added,
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
        "message": f"Added elements to {target}."
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 Starting Stacks & Queues Visual Simulator on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
