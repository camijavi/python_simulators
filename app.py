"""
Flask Application for Stacks, Queues, and Sorted Linked Lists Visual Simulator.
Provides RESTful APIs for Stack (LIFO), Queue (FIFO), and Sorted Linked List.
Maintains internal architecture in English and displays messages to user in Spanish.
"""

import os
import uuid
import random
from flask import Flask, render_template, request, jsonify, session
from structures import (
    Stack,
    Queue,
    SortedLinkedList,
    StackOverflowError,
    StackUnderflowError,
    QueueOverflowError,
    QueueUnderflowError,
    DuplicateValueError,
    LinkedListUnderflowError,
    NodeNotFoundError,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-simulators-2026")

# In-memory store for session-based simulators
# Structure: {session_id: {"stack": Stack(), "queue": Queue(), "linked_list": SortedLinkedList()}}
SIMULATOR_STORE = {}

SAMPLE_VALUES = [
    "Plato 1", "Plato 2", "Libro A", "Tarjeta 10", "Ficha X",
    "Tarea 101", "Trabajo 404", "Bloque 7", "Paquete 3", "Dato 8"
]

SAMPLE_NUMBERS = [10, 25, 5, 42, 17, 88, 3, 50, 64, 31, 72, 9]


def get_simulator():
    """Retrieve or initialize the Stack, Queue, and SortedLinkedList for the current session."""
    if "session_id" not in session or session["session_id"] not in SIMULATOR_STORE:
        session["session_id"] = str(uuid.uuid4())
        SIMULATOR_STORE[session["session_id"]] = {
            "stack": Stack(capacity=7),
            "queue": Queue(capacity=7),
            "linked_list": SortedLinkedList(capacity=7),
        }
    return SIMULATOR_STORE[session["session_id"]]


@app.route("/")
def index():
    """Serve the main simulator visual interface."""
    get_simulator()
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    """Return the current serialized state of Stack, Queue, and SortedLinkedList."""
    sim = get_simulator()
    return jsonify({
        "success": True,
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
        "linked_list": sim["linked_list"].to_dict(),
        "stack_history": sim["stack"].history[-10:],
        "queue_history": sim["queue"].history[-10:],
        "linked_list_history": sim["linked_list"].history[-10:],
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
            "message": f"Capacidad de la pila ajustada a {new_cap}."
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
            "message": f"Capacidad de la cola ajustada a {new_cap}."
        })
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ==========================================
# Sorted Linked List Endpoints
# Reference: read.me
# ==========================================

@app.route("/api/linked_list/insert", methods=["POST"])
def linked_list_insert():
    """Insert node in sorted ascending order. Rejects duplicates."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    val = data.get("value")

    if val is None or str(val).strip() == "":
        existing = sim["linked_list"].to_list()
        candidates = [n for n in SAMPLE_NUMBERS if n not in existing]
        val = random.choice(candidates) if candidates else random.randint(1, 99)

    try:
        record = sim["linked_list"].insert(val)
        return jsonify({
            "success": True,
            "operation": record,
            "linked_list": sim["linked_list"].to_dict(),
            "message": record["message"]
        })
    except (DuplicateValueError, StackOverflowError) as e:
        return jsonify({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e),
            "linked_list": sim["linked_list"].to_dict()
        }), 400


@app.route("/api/linked_list/remove_head", methods=["POST"])
def linked_list_remove_head():
    """Remove the head node."""
    sim = get_simulator()
    try:
        record = sim["linked_list"].remove_head()
        return jsonify({
            "success": True,
            "operation": record,
            "linked_list": sim["linked_list"].to_dict(),
            "message": record["message"]
        })
    except LinkedListUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "LinkedListUnderflowError",
            "message": str(e),
            "linked_list": sim["linked_list"].to_dict()
        }), 400


@app.route("/api/linked_list/remove_tail", methods=["POST"])
def linked_list_remove_tail():
    """Remove the last node."""
    sim = get_simulator()
    try:
        record = sim["linked_list"].remove_tail()
        return jsonify({
            "success": True,
            "operation": record,
            "linked_list": sim["linked_list"].to_dict(),
            "message": record["message"]
        })
    except LinkedListUnderflowError as e:
        return jsonify({
            "success": False,
            "error_type": "LinkedListUnderflowError",
            "message": str(e),
            "linked_list": sim["linked_list"].to_dict()
        }), 400


@app.route("/api/linked_list/remove_value", methods=["POST"])
def linked_list_remove_value():
    """Remove a specific node by value."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    val = data.get("value")

    if val is None or str(val).strip() == "":
        return jsonify({"success": False, "message": "Debe especificar un valor para eliminar."}), 400

    try:
        record = sim["linked_list"].remove_value(val)
        return jsonify({
            "success": True,
            "operation": record,
            "linked_list": sim["linked_list"].to_dict(),
            "message": record["message"]
        })
    except (LinkedListUnderflowError, NodeNotFoundError) as e:
        return jsonify({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e),
            "linked_list": sim["linked_list"].to_dict()
        }), 400


@app.route("/api/linked_list/search", methods=["POST"])
def linked_list_search():
    """Search for a value in the linked list."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    val = data.get("value")

    if val is None or str(val).strip() == "":
        return jsonify({"success": False, "message": "Debe especificar un valor a buscar."}), 400

    try:
        record = sim["linked_list"].search(val)
        return jsonify({
            "success": True,
            "operation": record,
            "linked_list": sim["linked_list"].to_dict(),
            "message": record["message"]
        })
    except (LinkedListUnderflowError, NodeNotFoundError) as e:
        return jsonify({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e),
            "linked_list": sim["linked_list"].to_dict()
        }), 400


@app.route("/api/linked_list/clear", methods=["POST"])
def linked_list_clear():
    """Clear all nodes from the linked list."""
    sim = get_simulator()
    record = sim["linked_list"].clear()
    return jsonify({
        "success": True,
        "operation": record,
        "linked_list": sim["linked_list"].to_dict(),
        "message": record["message"]
    })


@app.route("/api/linked_list/capacity", methods=["POST"])
def linked_list_capacity():
    """Update linked list capacity."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    try:
        new_cap = int(data.get("capacity", 7))
        sim["linked_list"].set_capacity(new_cap)
        return jsonify({
            "success": True,
            "capacity": sim["linked_list"].capacity,
            "linked_list": sim["linked_list"].to_dict(),
            "message": f"Capacidad de la lista ajustada a {new_cap}."
        })
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ==========================================
# Bulk & Reset Utilities
# ==========================================

@app.route("/api/reset", methods=["POST"])
def reset_all():
    """Reset stack, queue, and linked list to empty state."""
    sim = get_simulator()
    sim["stack"].clear()
    sim["queue"].clear()
    sim["linked_list"].clear()
    sim["stack"].history.clear()
    sim["queue"].history.clear()
    sim["linked_list"].history.clear()
    return jsonify({
        "success": True,
        "message": "Pila, cola y lista enlazada han sido reiniciadas.",
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
        "linked_list": sim["linked_list"].to_dict(),
    })


@app.route("/api/bulk_fill", methods=["POST"])
def bulk_fill():
    """Fill stack, queue, and/or linked list with random values."""
    sim = get_simulator()
    data = request.get_json(silent=True) or {}
    target = data.get("target", "all")
    count = min(int(data.get("count", 3)), 5)
    added = {"stack": [], "queue": [], "linked_list": []}

    if target in ("stack", "all"):
        for _ in range(count):
            if not sim["stack"].is_full():
                val = random.choice(SAMPLE_VALUES)
                sim["stack"].push(val)
                added["stack"].append(val)

    if target in ("queue", "all"):
        for _ in range(count):
            if not sim["queue"].is_full():
                val = random.choice(SAMPLE_VALUES)
                sim["queue"].enqueue(val)
                added["queue"].append(val)

    if target in ("linked_list", "all"):
        current_list = sim["linked_list"].to_list()
        candidates = [n for n in SAMPLE_NUMBERS if n not in current_list]
        random.shuffle(candidates)
        for val in candidates[:count]:
            if not sim["linked_list"].is_full():
                try:
                    sim["linked_list"].insert(val)
                    added["linked_list"].append(val)
                except DuplicateValueError:
                    pass

    return jsonify({
        "success": True,
        "added": added,
        "stack": sim["stack"].to_dict(),
        "queue": sim["queue"].to_dict(),
        "linked_list": sim["linked_list"].to_dict(),
        "message": f"Elementos agregados aleatoriamente."
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 Iniciando Simulador Visual en http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
