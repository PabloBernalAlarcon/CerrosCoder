// Runs Python (Pyodide) in a background thread, so an infinite loop never
// freezes the page: py-runner.js simply stops this worker and starts a new one.
const PYODIDE_VERSION = "0.26.4";
importScripts(`https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`);

const listo = (async () => {
  const pyodide = await loadPyodide();
  const respuesta = await fetch("harness.py", { cache: "no-cache" });
  if (!respuesta.ok) throw new Error("No se encontró js/harness.py");
  pyodide.runPython(await respuesta.text());
  return pyodide;
})();

listo.then(
  () => self.postMessage({ type: "ready" }),
  (err) => self.postMessage({ type: "fatal", error: String(err) })
);

self.onmessage = async (event) => {
  const { id, ...peticion } = event.data;
  try {
    const pyodide = await listo;
    pyodide.globals.set("_peticion", JSON.stringify(peticion));
    const texto = pyodide.runPython("_atender(_peticion)");
    self.postMessage({ type: "result", id, result: JSON.parse(texto) });
  } catch (err) {
    self.postMessage({ type: "result", id, result: { internalError: String(err) } });
  }
};
