/**
 * Simulador Visual Interactivo: Pilas, Colas y Listas Enlazadas
 * Maneja navegación por pestañas individuales, animaciones en el DOM,
 * efectos de sonido Web Audio API y comunicación con Flask API.
 */

// Paleta de gradientes para bloques inspirada en el logo PyData Visualizer
const ITEM_GRADIENTS = [
  "linear-gradient(135deg, #FFA9C2 0%, #F472B6 100%)", // Rosa Pastel (Disco Superior Pila)
  "linear-gradient(135deg, #FCB075 0%, #FB923C 100%)", // Melocotón Cálido (Bloque Cola / Data)
  "linear-gradient(135deg, #FDDA76 0%, #FBBF24 100%)", // Amarillo Pastel (Bloque Cola / Serpiente)
  "linear-gradient(135deg, #A7EDC1 0%, #34D399 100%)", // Verde Menta (Nodo Lista / Py)
  "linear-gradient(135deg, #76B6F0 0%, #38BDF8 100%)", // Azul Cielo (Bloque Cola / Nodo 2)
  "linear-gradient(135deg, #CFA7F4 0%, #A78BFA 100%)", // Lavanda / Orquídea (Disco Medio Pila / Visualizer)
  "linear-gradient(135deg, #93C5FD 0%, #60A5FA 100%)", // Azul Periwinkle (Disco Inferior Pila)
  "linear-gradient(135deg, #A9DBF4 0%, #7DD3FC 100%)", // Celeste Suave
];

const SAMPLE_NAMES = [
  "Plato 1", "Plato 2", "Libro A", "Tarjeta 10", "Ficha X",
  "Tarea 101", "Trabajo 404", "Bloque 7", "Paquete 3", "Dato 8"
];

const CANDIDATE_NUMBERS = [10, 25, 5, 42, 17, 88, 3, 50, 64, 31, 72, 9, 15, 33, 99];

// Sintetizador de audio Web Audio API
class SoundFX {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
  }

  playTone(freq, type = "sine", duration = 0.15, gainVal = 0.1) {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      console.warn("Audio error:", e);
    }
  }

  push() {
    this.playTone(320, "triangle", 0.1, 0.15);
    setTimeout(() => this.playTone(480, "triangle", 0.15, 0.12), 60);
  }

  pop() {
    this.playTone(480, "triangle", 0.1, 0.15);
    setTimeout(() => this.playTone(280, "triangle", 0.15, 0.12), 60);
  }

  peek() {
    this.playTone(660, "sine", 0.25, 0.15);
  }

  error() {
    this.playTone(180, "sawtooth", 0.25, 0.2);
  }

  clear() {
    this.playTone(220, "sine", 0.15, 0.15);
  }
}

const sfx = new SoundFX();

// Estado principal de la aplicación
const App = {
  stackItems: [],
  queueItems: [],
  listItems: [],
  stackCapacity: 7,
  queueCapacity: 7,
  listCapacity: 7,
  animDurationMs: 600,

  init() {
    this.bindEvents();
    this.fetchInitialState();
  },

  bindEvents() {
    // Alternar Sonido
    const soundToggle = document.getElementById("soundToggle");
    soundToggle.addEventListener("click", () => {
      sfx.enabled = !sfx.enabled;
      soundToggle.querySelector(".sound-text").textContent = `Sonido: ${sfx.enabled ? "ACTIVO" : "SILENCIADO"}`;
      soundToggle.style.opacity = sfx.enabled ? "1" : "0.6";
    });

    // Selector de Velocidad
    const speedSelect = document.getElementById("animationSpeed");
    speedSelect.addEventListener("change", (e) => {
      const val = parseFloat(e.target.value);
      this.animDurationMs = val * 1000;
      document.documentElement.style.setProperty("--anim-speed", `${val}s`);
    });

    // ================= Navegación de Pestañas de Simuladores =================
    const simTabBtns = document.querySelectorAll(".sim-tab-btn");
    const simPanels = {
      stack: document.getElementById("stackSection"),
      queue: document.getElementById("queueSection"),
      linkedlist: document.getElementById("linkedListSection")
    };

    simTabBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        simTabBtns.forEach(b => {
          b.classList.remove("active");
          b.setAttribute("aria-selected", "false");
        });
        btn.classList.add("active");
        btn.setAttribute("aria-selected", "true");

        const target = btn.dataset.sim;
        Object.keys(simPanels).forEach(key => {
          if (simPanels[key]) {
            if (key === target) {
              simPanels[key].classList.add("active");
            } else {
              simPanels[key].classList.remove("active");
            }
          }
        });
      });
    });

    // ================= Pestañas Educativas Inferiores =================
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        btn.classList.add("active");
        const tabId = `tab-${btn.dataset.tab}`;
        const target = document.getElementById(tabId);
        if (target) target.classList.add("active");
      });
    });

    // Controles Globales
    document.getElementById("resetAllBtn").addEventListener("click", () => this.resetAll());
    document.getElementById("bulkFillBtn").addEventListener("click", () => this.bulkFill());

    // ================= Controles de Pila =================
    document.getElementById("stackPushBtn").addEventListener("click", () => this.stackPush());
    document.getElementById("stackPopBtn").addEventListener("click", () => this.stackPop());
    document.getElementById("stackPeekBtn").addEventListener("click", () => this.stackPeek());
    document.getElementById("stackClearBtn").addEventListener("click", () => this.stackClear());
    document.getElementById("stackRandomBtn").addEventListener("click", () => {
      document.getElementById("stackInput").value = this.getRandomSample();
    });
    document.getElementById("stackInput").addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.stackPush();
    });

    // ================= Controles de Cola =================
    document.getElementById("queueEnqueueBtn").addEventListener("click", () => this.queueEnqueue());
    document.getElementById("queueDequeueBtn").addEventListener("click", () => this.queueDequeue());
    document.getElementById("queuePeekBtn").addEventListener("click", () => this.queuePeek());
    document.getElementById("queueClearBtn").addEventListener("click", () => this.queueClear());
    document.getElementById("queueRandomBtn").addEventListener("click", () => {
      document.getElementById("queueInput").value = this.getRandomSample();
    });
    document.getElementById("queueInput").addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.queueEnqueue();
    });

    // ================= Controles de Lista Enlazada =================
    document.getElementById("listInsertBtn").addEventListener("click", () => this.listInsert());
    document.getElementById("listRemoveHeadBtn").addEventListener("click", () => this.listRemoveHead());
    document.getElementById("listRemoveTailBtn").addEventListener("click", () => this.listRemoveTail());
    document.getElementById("listRemoveValBtn").addEventListener("click", () => this.listRemoveValue());
    document.getElementById("listSearchBtn").addEventListener("click", () => this.listSearch());
    document.getElementById("listClearBtn").addEventListener("click", () => this.listClear());
    document.getElementById("listRandomBtn").addEventListener("click", () => {
      document.getElementById("listInput").value = this.getRandomUniqueNumber();
    });
    document.getElementById("listInput").addEventListener("keydown", (e) => {
      if (e.key === "Enter") this.listInsert();
    });
  },

  getRandomSample() {
    return SAMPLE_NAMES[Math.floor(Math.random() * SAMPLE_NAMES.length)];
  },

  getRandomUniqueNumber() {
    const available = CANDIDATE_NUMBERS.filter(n => !this.listItems.includes(n));
    if (available.length > 0) {
      return available[Math.floor(Math.random() * available.length)];
    }
    return Math.floor(Math.random() * 90) + 10;
  },

  getItemGradient(idx) {
    return ITEM_GRADIENTS[idx % ITEM_GRADIENTS.length];
  },

  async fetchInitialState() {
    try {
      const res = await fetch("/api/state");
      const data = await res.json();
      if (data.success) {
        this.stackCapacity = 7;
        this.queueCapacity = 7;
        this.listCapacity = 7;

        this.renderStack(data.stack);
        this.renderQueue(data.queue);
        this.renderLinkedList(data.linked_list);
      }
    } catch (err) {
      console.error("Error al cargar estado inicial:", err);
    }
  },

  // ==========================================
  // Lógica UI de Pila (Stack)
  // ==========================================
  async stackPush() {
    const input = document.getElementById("stackInput");
    let val = input.value.trim();
    if (!val) val = this.getRandomSample();

    try {
      const res = await fetch("/api/stack/push", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: val })
      });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("stackAlert", data.message, "alert-error");
        return;
      }

      input.value = "";
      sfx.push();
      this.clearAlert("stackAlert");
      this.renderStack(data.stack, { animatedAction: "push" });
    } catch (err) {
      console.error("Error en Push:", err);
    }
  },

  async stackPop() {
    if (this.stackItems.length === 0) {
      sfx.error();
      this.showAlert("stackAlert", "¡Subdesbordamiento! La pila está vacía (no se puede desapilar).", "alert-error");
      return;
    }

    const container = document.getElementById("stackItems");
    const topNode = container.lastElementChild;
    if (topNode) topNode.classList.add("anim-pop");

    sfx.pop();

    setTimeout(async () => {
      try {
        const res = await fetch("/api/stack/pop", { method: "POST" });
        const data = await res.json();

        if (!res.ok || !data.success) {
          sfx.error();
          this.showAlert("stackAlert", data.message, "alert-error");
          return;
        }

        this.clearAlert("stackAlert");
        this.renderStack(data.stack);
      } catch (err) {
        console.error("Error en Pop:", err);
      }
    }, this.animDurationMs * 0.7);
  },

  async stackPeek() {
    try {
      const res = await fetch("/api/stack/peek");
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("stackAlert", data.message, "alert-error");
        return;
      }

      sfx.peek();
      this.showAlert("stackAlert", `Elemento en la Cima: '${data.operation.element}' (índice ${data.operation.index})`, "alert-info");

      const container = document.getElementById("stackItems");
      const topNode = container.lastElementChild;
      if (topNode) {
        topNode.classList.remove("item-peek");
        void topNode.offsetWidth;
        topNode.classList.add("item-peek");
        setTimeout(() => topNode.classList.remove("item-peek"), 2000);
      }
    } catch (err) {
      console.error("Error en Peek:", err);
    }
  },

  async stackClear() {
    try {
      const res = await fetch("/api/stack/clear", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        sfx.clear();
        this.clearAlert("stackAlert");
        this.renderStack(data.stack);
      }
    } catch (err) {
      console.error("Error al vaciar pila:", err);
    }
  },

  async setStackCapacity(cap) {
    try {
      const res = await fetch("/api/stack/capacity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ capacity: cap })
      });
      const data = await res.json();
      if (!res.ok) {
        sfx.error();
        this.showAlert("stackAlert", data.message, "alert-error");
        document.getElementById("stackCapacitySlider").value = this.stackCapacity;
      } else {
        this.stackCapacity = data.capacity;
        document.getElementById("stackCapVal").textContent = cap;
        this.clearAlert("stackAlert");
        this.renderStack(data.stack);
      }
    } catch (err) {
      console.error("Error en capacidad de pila:", err);
    }
  },

  renderStack(stackState, animOpts = {}) {
    this.stackItems = stackState.items;
    this.stackCapacity = stackState.capacity;
    const container = document.getElementById("stackItems");
    const emptyState = document.getElementById("stackEmptyState");
    const topPointer = document.getElementById("stackTopPointer");

    document.getElementById("stackCapacityPill").textContent = `Capacidad: ${stackState.capacity}`;
    document.getElementById("stackSizePill").textContent = `Tamaño: ${stackState.size} / ${stackState.capacity}`;
    document.getElementById("stackIsEmpty").textContent = stackState.is_empty ? "Sí" : "No";
    document.getElementById("stackIsFull").textContent = stackState.is_full ? "Sí" : "No";
    document.getElementById("stackTopVal").textContent = stackState.top_element !== null ? stackState.top_element : "Ninguno";

    container.innerHTML = "";

    if (stackState.items.length === 0) {
      emptyState.classList.remove("hidden");
      topPointer.classList.add("hidden");
      return;
    }

    emptyState.classList.add("hidden");

    stackState.items.forEach((itemVal, idx) => {
      const block = document.createElement("div");
      block.className = "data-item";
      block.style.background = this.getItemGradient(idx);

      if (animOpts.animatedAction === "push" && idx === stackState.items.length - 1) {
        block.classList.add("anim-push");
      }

      block.innerHTML = `
        <span class="item-value-text" title="${itemVal}">${itemVal}</span>
        <span class="item-index-badge">i: ${idx}</span>
      `;
      container.appendChild(block);
    });

    topPointer.classList.remove("hidden");
    document.getElementById("stackTopIdx").textContent = stackState.top_index;

    const itemHeight = 35;
    const bottomOffset = 8 + (stackState.items.length - 1) * itemHeight + 8;
    topPointer.style.top = `${280 - bottomOffset}px`;
  },

  // ==========================================
  // Lógica UI de Cola (Queue)
  // ==========================================
  async queueEnqueue() {
    const input = document.getElementById("queueInput");
    let val = input.value.trim();
    if (!val) val = this.getRandomSample();

    try {
      const res = await fetch("/api/queue/enqueue", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: val })
      });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("queueAlert", data.message, "alert-error");
        return;
      }

      input.value = "";
      sfx.push();
      this.clearAlert("queueAlert");
      this.renderQueue(data.queue, { animatedAction: "enqueue" });
    } catch (err) {
      console.error("Error en Enqueue:", err);
    }
  },

  async queueDequeue() {
    if (this.queueItems.length === 0) {
      sfx.error();
      this.showAlert("queueAlert", "¡Subdesbordamiento! La cola está vacía (no se puede desencolar).", "alert-error");
      return;
    }

    const container = document.getElementById("queueItems");
    const frontNode = container.firstElementChild;
    if (frontNode) frontNode.classList.add("anim-dequeue");

    sfx.pop();

    setTimeout(async () => {
      try {
        const res = await fetch("/api/queue/dequeue", { method: "POST" });
        const data = await res.json();

        if (!res.ok || !data.success) {
          sfx.error();
          this.showAlert("queueAlert", data.message, "alert-error");
          return;
        }

        this.clearAlert("queueAlert");
        this.renderQueue(data.queue);
      } catch (err) {
        console.error("Error en Dequeue:", err);
      }
    }, this.animDurationMs * 0.7);
  },

  async queuePeek() {
    try {
      const res = await fetch("/api/queue/peek");
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("queueAlert", data.message, "alert-error");
        return;
      }

      sfx.peek();
      this.showAlert("queueAlert", `Frente de la Cola: '${data.operation.element}' (índice 0)`, "alert-info");

      const container = document.getElementById("queueItems");
      const frontNode = container.firstElementChild;
      if (frontNode) {
        frontNode.classList.remove("item-peek");
        void frontNode.offsetWidth;
        frontNode.classList.add("item-peek");
        setTimeout(() => frontNode.classList.remove("item-peek"), 2000);
      }
    } catch (err) {
      console.error("Error en Queue Peek:", err);
    }
  },

  async queueClear() {
    try {
      const res = await fetch("/api/queue/clear", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        sfx.clear();
        this.clearAlert("queueAlert");
        this.renderQueue(data.queue);
      }
    } catch (err) {
      console.error("Error al vaciar cola:", err);
    }
  },

  async setQueueCapacity(cap) {
    try {
      const res = await fetch("/api/queue/capacity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ capacity: cap })
      });
      const data = await res.json();
      if (!res.ok) {
        sfx.error();
        this.showAlert("queueAlert", data.message, "alert-error");
        document.getElementById("queueCapacitySlider").value = this.queueCapacity;
      } else {
        this.queueCapacity = data.capacity;
        document.getElementById("queueCapVal").textContent = cap;
        this.clearAlert("queueAlert");
        this.renderQueue(data.queue);
      }
    } catch (err) {
      console.error("Error en capacidad de cola:", err);
    }
  },

  renderQueue(queueState, animOpts = {}) {
    this.queueItems = queueState.items;
    this.queueCapacity = queueState.capacity;
    const container = document.getElementById("queueItems");
    const emptyState = document.getElementById("queueEmptyState");
    const frontPointer = document.getElementById("queueFrontPointer");
    const rearPointer = document.getElementById("queueRearPointer");

    document.getElementById("queueCapacityPill").textContent = `Capacidad: ${queueState.capacity}`;
    document.getElementById("queueSizePill").textContent = `Tamaño: ${queueState.size} / ${queueState.capacity}`;
    document.getElementById("queueIsEmpty").textContent = queueState.is_empty ? "Sí" : "No";
    document.getElementById("queueIsFull").textContent = queueState.is_full ? "Sí" : "No";
    document.getElementById("queueFrontVal").textContent = queueState.front_element !== null ? queueState.front_element : "Ninguno";
    document.getElementById("queueRearVal").textContent = queueState.rear_element !== null ? queueState.rear_element : "Ninguno";

    container.innerHTML = "";

    if (queueState.items.length === 0) {
      emptyState.classList.remove("hidden");
      frontPointer.classList.add("hidden");
      rearPointer.classList.add("hidden");
      return;
    }

    emptyState.classList.add("hidden");

    queueState.items.forEach((itemVal, idx) => {
      const block = document.createElement("div");
      block.className = "queue-item";
      block.style.background = this.getItemGradient(idx);

      if (animOpts.animatedAction === "enqueue" && idx === queueState.items.length - 1) {
        block.classList.add("anim-enqueue");
      }

      block.innerHTML = `
        <span class="item-value-text" title="${itemVal}">${itemVal}</span>
        <span class="item-index-badge">i: ${idx}</span>
      `;
      container.appendChild(block);
    });

    const itemSpacing = 70;
    const offset = 12;

    frontPointer.classList.remove("hidden");
    frontPointer.style.left = `${offset + 12}px`;

    rearPointer.classList.remove("hidden");
    const rearX = offset + (queueState.items.length - 1) * itemSpacing + 12;
    rearPointer.style.left = `${rearX}px`;
  },

  // ==========================================
  // Lógica UI de Lista Enlazada (Linked List)
  // ==========================================
  async listInsert() {
    const input = document.getElementById("listInput");
    let val = input.value.trim();
    if (!val) val = this.getRandomUniqueNumber();

    try {
      const res = await fetch("/api/linked_list/insert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: val })
      });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        return;
      }

      input.value = "";
      sfx.push();
      this.clearAlert("listAlert");
      this.renderLinkedList(data.linked_list, { insertedValue: data.operation.element });
    } catch (err) {
      console.error("Error en Insertar Lista:", err);
    }
  },

  async listRemoveHead() {
    if (this.listItems.length === 0) {
      sfx.error();
      this.showAlert("listAlert", "La lista enlazada está vacía. No se puede quitar la cabeza.", "alert-error");
      return;
    }

    sfx.pop();
    try {
      const res = await fetch("/api/linked_list/remove_head", { method: "POST" });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        return;
      }

      this.clearAlert("listAlert");
      this.renderLinkedList(data.linked_list);
    } catch (err) {
      console.error("Error al quitar cabeza:", err);
    }
  },

  async listRemoveTail() {
    if (this.listItems.length === 0) {
      sfx.error();
      this.showAlert("listAlert", "La lista enlazada está vacía. No se puede quitar la cola.", "alert-error");
      return;
    }

    sfx.pop();
    try {
      const res = await fetch("/api/linked_list/remove_tail", { method: "POST" });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        return;
      }

      this.clearAlert("listAlert");
      this.renderLinkedList(data.linked_list);
    } catch (err) {
      console.error("Error al quitar cola:", err);
    }
  },

  async listRemoveValue() {
    const input = document.getElementById("listInput");
    const val = input.value.trim();

    if (!val) {
      sfx.error();
      this.showAlert("listAlert", "Por favor ingresa el valor numérico del nodo a eliminar.", "alert-error");
      return;
    }

    try {
      const res = await fetch("/api/linked_list/remove_value", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: val })
      });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        return;
      }

      input.value = "";
      sfx.pop();
      this.clearAlert("listAlert");
      this.renderLinkedList(data.linked_list);
    } catch (err) {
      console.error("Error al quitar valor:", err);
    }
  },

  async listSearch() {
    const input = document.getElementById("listInput");
    const val = input.value.trim();

    if (!val) {
      sfx.error();
      this.showAlert("listAlert", "Por favor ingresa el valor a buscar en la lista.", "alert-error");
      return;
    }

    try {
      const res = await fetch("/api/linked_list/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value: val })
      });
      const data = await res.json();

      if (!res.ok || !data.success) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        return;
      }

      sfx.peek();
      this.showAlert("listAlert", `Resultado: ${data.operation.message}`, "alert-info");

      const container = document.getElementById("listChain");
      const targetNode = container.children[data.operation.index];
      if (targetNode) {
        const innerNode = targetNode.querySelector(".linked-node");
        if (innerNode) {
          innerNode.classList.remove("item-peek");
          void innerNode.offsetWidth;
          innerNode.classList.add("item-peek");
          setTimeout(() => innerNode.classList.remove("item-peek"), 2500);
        }
      }
    } catch (err) {
      console.error("Error al buscar en lista:", err);
    }
  },

  async listClear() {
    try {
      const res = await fetch("/api/linked_list/clear", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        sfx.clear();
        this.clearAlert("listAlert");
        this.renderLinkedList(data.linked_list);
      }
    } catch (err) {
      console.error("Error al vaciar lista:", err);
    }
  },

  async setListCapacity(cap) {
    try {
      const res = await fetch("/api/linked_list/capacity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ capacity: cap })
      });
      const data = await res.json();
      if (!res.ok) {
        sfx.error();
        this.showAlert("listAlert", data.message, "alert-error");
        document.getElementById("listCapacitySlider").value = this.listCapacity;
      } else {
        this.listCapacity = data.capacity;
        document.getElementById("listCapVal").textContent = cap;
        this.clearAlert("listAlert");
        this.renderLinkedList(data.linked_list);
      }
    } catch (err) {
      console.error("Error en capacidad de lista:", err);
    }
  },

  renderLinkedList(listState, animOpts = {}) {
    this.listItems = listState.items;
    this.listCapacity = listState.capacity;
    const container = document.getElementById("listChain");
    const emptyState = document.getElementById("listEmptyState");

    document.getElementById("listCapacityPill").textContent = `Capacidad: ${listState.capacity}`;
    document.getElementById("listSizePill").textContent = `Nodos: ${listState.size} / ${listState.capacity}`;
    document.getElementById("listIsEmpty").textContent = listState.is_empty ? "Sí" : "No";
    document.getElementById("listHeadVal").textContent = listState.head !== null ? listState.head : "NULL";
    document.getElementById("listTailVal").textContent = listState.tail !== null ? listState.tail : "NULL";

    container.innerHTML = "";

    if (listState.nodes.length === 0) {
      emptyState.classList.remove("hidden");
      return;
    }

    emptyState.classList.add("hidden");

    listState.nodes.forEach((node, idx) => {
      const wrapper = document.createElement("div");
      wrapper.className = "node-wrapper";

      let headTag = "";
      if (node.is_head) {
        headTag = `<span class="node-head-badge">HEAD (Cabeza)</span>`;
      }

      let insertClass = "";
      if (animOpts.insertedValue !== undefined && node.value === animOpts.insertedValue) {
        insertClass = "anim-node-insert";
      }

      wrapper.innerHTML = `
        ${headTag}
        <div class="linked-node ${insertClass}">
          <div class="node-data-box">
            <span>${node.value}</span>
            <span class="node-idx-sub">#${idx}</span>
          </div>
          <div class="node-pointer-box">
            <span>next ➔</span>
          </div>
        </div>
        <span class="node-arrow">──►</span>
      `;
      container.appendChild(wrapper);
    });

    const nullNode = document.createElement("div");
    nullNode.className = "null-node";
    nullNode.textContent = "⊘ NULL";
    container.appendChild(nullNode);
  },

  // ==========================================
  // Acciones Globales
  // ==========================================
  async bulkFill() {
    try {
      const res = await fetch("/api/bulk_fill", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: "all", count: 3 })
      });
      const data = await res.json();
      if (data.success) {
        sfx.push();
        this.renderStack(data.stack);
        this.renderQueue(data.queue);
        this.renderLinkedList(data.linked_list);
      }
    } catch (err) {
      console.error("Error en llenado rápido:", err);
    }
  },

  async resetAll() {
    try {
      const res = await fetch("/api/reset", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        sfx.clear();
        this.clearAlert("stackAlert");
        this.clearAlert("queueAlert");
        this.clearAlert("listAlert");
        this.renderStack(data.stack);
        this.renderQueue(data.queue);
        this.renderLinkedList(data.linked_list);
      }
    } catch (err) {
      console.error("Error al reiniciar todo:", err);
    }
  },

  showAlert(alertId, message, alertClass) {
    const alertEl = document.getElementById(alertId);
    if (!alertEl) return;
    alertEl.className = `alert-box ${alertClass}`;
    alertEl.textContent = message;
    alertEl.classList.remove("hidden");

    setTimeout(() => {
      alertEl.classList.add("hidden");
    }, 4500);
  },

  clearAlert(alertId) {
    const alertEl = document.getElementById(alertId);
    if (alertEl) alertEl.classList.add("hidden");
  }
};

// Iniciar aplicación cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  App.init();
});
