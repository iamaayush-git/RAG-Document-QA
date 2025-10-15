// backend/src/services/pythonClient.js
import fetch from "node-fetch";

const PY_URL = process.env.PYTHON_URL || "http://localhost:8001";

export async function callPythonIngest(filepath) {
  const resp = await fetch(`${PY_URL}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filepath }),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Python ingest failed: ${resp.status} ${text}`);
  }
  return resp.json();
}

export async function callPythonAsk(question, k = 4) {
  const resp = await fetch(`${PY_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, k }),
  });
  if (!resp.ok) throw new Error("Python ask failed");
  return resp.json();
}
