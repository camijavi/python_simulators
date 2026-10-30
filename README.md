# 🥞 Simulador Visual: Pilas, Colas y Listas Enlazadas (Stacks, Queues & Sorted Linked Lists)

> **Made by Camila Navarro & Francis Solorzano**

Un simulador web educativo e interactivo desarrollado en **Python** y **Flask** que visualiza en tiempo real las operaciones, punteros y comportamiento en memoria de tres estructuras de datos fundamentales:
- **Pilas (Stacks - LIFO)**
- **Colas (Queues - FIFO)**
- **Listas Enlazadas Ordenadas (Sorted Singly Linked Lists)** con base en los principios teóricos del aula (`read.me`).

> La interfaz y mensajes mostrados al usuario se presentan en **español**, mientras que la arquitectura de código interno, clases, APIs y pruebas se mantienen en **inglés**.

---

## 🌟 Características Principales

### 1. Pila (Stack - LIFO)
- **Principio**: *Last-In, First-Out* (Último en Entrar, Primero en Salir).
- **Contenedor Visual**: Vaso de precipitados con fondo cerrado y tope abierto.
- **Operaciones**: `Push` (animación de caída), `Pop` (animación de elevación), `Peek` (resaltado pulsante de cima), y `Vaciar`.
- **Punteros**: Puntero reactivo `TOPE` que sigue la cima en tiempo real.
- **Protección**: Alertas visuales de *Stack Overflow* (desbordamiento) y *Stack Underflow* (subdesbordamiento).

### 2. Cola (Queue - FIFO)
- **Principio**: *First-In, First-Out* (Primero en Entrar, Primero en Salir).
- **Contenedor Visual**: Cinta transportadora / tubería horizontal con dirección de flujo.
- **Operaciones**: `Enqueue` (entrada por el Final), `Dequeue` (salida por el Frente), `Peek` (frente), y `Vaciar`.
- **Punteros**: Doble puntero: `FRENTE` (índice 0) y `FINAL` (índice $n-1$).
- **Protección**: Alertas de *Queue Overflow* y *Queue Underflow*.

### 3. Lista Enlazada Ordenada (Sorted Linked List)
*Implementada conforme a la teoría de clase (`read.me`):*
- **Inserción**: Ubica automáticamente el nodo en la posición exacta para mantener el **orden ascendente**.
- **Sin valores repetidos**: Rechaza duplicados (`DuplicateValueError`) para garantizar unicidad.
- **Eliminación organizada**: Permite eliminar por cabeza (`remove_head`), eliminar por cola (`remove_tail`) o eliminar un nodo por valor específico (`remove_value`). En todos los casos la lista permanece ordenada.
- **Búsqueda**: Operación `search` que recorre y reporta la posición exacta y número de comparaciones.
- **Representación Visual**:
  - Celda de memoria de dos compartimentos por nodo: `[ Valor | sig ➔ ]`.
  - Flechas de enlace reactivas (`──►`).
  - Distintivo para `HEAD (Cabeza)` y terminador `⊘ NULL`.

---

## 🏗️ Estructura del Proyecto

```
python_simulators/
├── app.py                 # Servidor Flask y endpoints REST
├── structures.py          # Implementaciones en Python: Stack, Queue, Node, SortedLinkedList
├── test_structures.py     # Pruebas unitarias de las estructuras de datos
├── test_api.py            # Pruebas de integración de la API REST
├── requirements.txt       # Dependencias (Flask)
├── read.me                # Notas teóricas de clase
├── README.md              # Documentación del proyecto
├── templates/
│   └── index.html         # Plantilla HTML5 con interfaz en español y pestañas educativas
└── static/
    ├── css/
    │   └── style.css      # Estilos modernos, diseño responsive y animaciones CSS
    └── js/
        └── app.js         # Lógica interactiva del cliente y efectos de sonido Web Audio
```

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
python3 app.py
```

### 3. Abrir en el Navegador
Visita:
```
http://127.0.0.1:5001
```

---

## 🧪 Pruebas Automatizadas

Ejecuta el conjunto completo de 25 pruebas unitarias e integración con:

```bash
python3 -m unittest discover
```

---

## 📡 Referencia de la API REST

| Endpoint | Método | Descripción |
| :--- | :---: | :--- |
| `GET /` | `GET` | Interfaz visual del simulador |
| `GET /api/state` | `GET` | Consulta el estado actual de pila, cola y lista enlazada |
| `POST /api/stack/push` | `POST` | Apila un valor (`{"value": "..."}`) |
| `POST /api/stack/pop` | `POST` | Desapila el elemento del tope |
| `GET /api/stack/peek` | `GET` | Inspecciona el tope |
| `POST /api/stack/clear` | `POST` | Vacía la pila |
| `POST /api/queue/enqueue` | `POST` | Encola un valor al final |
| `POST /api/queue/dequeue` | `POST` | Desencola el elemento del frente |
| `GET /api/queue/peek` | `GET` | Inspecciona el frente de la cola |
| `POST /api/queue/clear` | `POST` | Vacía la cola |
| `POST /api/linked_list/insert` | `POST` | Inserta valor en posición ascendente (sin duplicados) |
| `POST /api/linked_list/remove_head` | `POST` | Elimina la cabeza de la lista |
| `POST /api/linked_list/remove_tail` | `POST` | Elimina la cola de la lista |
| `POST /api/linked_list/remove_value`| `POST` | Elimina un nodo por su valor (`{"value": ...}`) |
| `POST /api/linked_list/search` | `POST` | Busca la posición de un valor |
| `POST /api/linked_list/clear` | `POST` | Vacía la lista enlazada |
| `POST /api/bulk_fill` | `POST` | Agrega elementos aleatorios a las 3 estructuras |
| `POST /api/reset` | `POST` | Reinicia todas las estructuras al estado vacío |

---

## ⏱️ Complejidad Temporal y Espacial

| Estructura | Inserción | Eliminación | Acceso / Búsqueda | Espacio |
| :--- | :---: | :---: | :---: | :---: |
| **Pila (Stack)** | $O(1)$ | $O(1)$ | $O(1)$ (Tope) | $O(N)$ |
| **Cola (Queue)** | $O(1)$ | $O(1)$ | $O(1)$ (Frente) | $O(N)$ |
| **Lista Enlazada Ordenada** | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
