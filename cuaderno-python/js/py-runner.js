// Small wrapper around py-worker.js with a time limit for each run.
const LIMITE_EJECUTAR_MS = 5000;
const LIMITE_COMPROBAR_MS = 10000;

export class PyRunner {
  // onStatus receives "cargando" | "listo" | "error"
  constructor({ onStatus = () => {} } = {}) {
    this.onStatus = onStatus;
    this.siguienteId = 1;
    this.pendientes = new Map();
    this._iniciar();
  }

  _iniciar() {
    this.onStatus("cargando");
    this.worker = new Worker("js/py-worker.js");
    this.listo = new Promise((resolve, reject) => {
      this.worker.onmessage = (event) => {
        const msg = event.data;
        if (msg.type === "ready") {
          this.onStatus("listo");
          resolve();
        } else if (msg.type === "fatal") {
          this.onStatus("error");
          reject(new Error(msg.error));
        } else if (msg.type === "result") {
          const pendiente = this.pendientes.get(msg.id);
          if (!pendiente) return;
          clearTimeout(pendiente.reloj);
          this.pendientes.delete(msg.id);
          pendiente.resolve(msg.result);
        }
      };
      this.worker.onerror = (event) => {
        this.onStatus("error");
        reject(new Error(event.message || "Error al cargar Python"));
      };
    });
    this.listo.catch(() => {}); // handled through onStatus
  }

  async _enviar(peticion, limiteMs) {
    await this.listo;
    const id = this.siguienteId++;
    return new Promise((resolve) => {
      const reloj = setTimeout(() => {
        // Too slow (probably an infinite loop): kill the worker and start fresh.
        this.pendientes.delete(id);
        this.worker.terminate();
        this._iniciar();
        resolve({ timeout: true, limiteSegundos: limiteMs / 1000 });
      }, limiteMs);
      this.pendientes.set(id, { resolve, reloj });
      this.worker.postMessage({ id, ...peticion });
    });
  }

  run(code, inputs = []) {
    return this._enviar({ mode: "run", code, inputs }, LIMITE_EJECUTAR_MS);
  }

  check(code, tests, prohibidos = []) {
    return this._enviar({ mode: "check", code, tests, prohibidos }, LIMITE_COMPROBAR_MS);
  }
}
