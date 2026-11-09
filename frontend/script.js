const API_BASE = "http://127.0.0.1:8000";
const API_URL = `${API_BASE}/api/chat`;
const form = document.querySelector("#chat-form");
const input = document.querySelector("#message");
const messages = document.querySelector("#messages");
const send = document.querySelector("#send");
const statusEl = document.querySelector(".status");
 
// route: "tfidf" = dijawab dari FAQ, "llm" = dijawab AI (RAG + Gemini)
function addMessage(text, role, sources = [], route = null) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  wrap.appendChild(bubble);
  if (route || sources.length) {
    const meta = document.createElement("div");
    meta.className = "meta";
    if (route) {
      const badge = document.createElement("span");
      badge.className = `badge badge-${route}`;
      badge.textContent = route === "tfidf" ? "FAQ" : "AI";
      meta.appendChild(badge);
    }
    if (sources.length) {
      const source = document.createElement("span");
      source.className = "sources";
      source.textContent = "Sumber: " + sources.join(", ");
      meta.appendChild(source);
    }
    wrap.appendChild(meta);
  }
  messages.appendChild(wrap);
  messages.scrollTop = messages.scrollHeight;
}
 
async function ask(question) {
  const message = question.trim();
  if (!message) return;
  addMessage(message, "user");
  input.value = "";
  send.disabled = true;
  send.textContent = "...";
  const pending = document.createElement("div");
  pending.className = "bubble bot";
  pending.textContent = "Sedang mencari informasi...";
  messages.appendChild(pending);
  messages.scrollTop = messages.scrollHeight;
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Terjadi kesalahan pada server.");
    pending.remove();
    addMessage(data.answer, "bot", data.sources || [], data.route);
  } catch (error) {
    pending.remove();
    addMessage("Maaf, layanan belum dapat dihubungi. Pastikan backend aktif dan API key Gemini sudah diatur. Detail: " + error.message, "bot");
  } finally {
    send.disabled = false;
    send.textContent = "Kirim";
    input.focus();
  }
}
 
// Perbarui indikator status di header dari /api/health
async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    const data = await response.json();
    statusEl.classList.remove("offline");
    statusEl.textContent = data.gemini_configured ? "● Online" : "● Online (tanpa Gemini)";
  } catch {
    statusEl.classList.add("offline");
    statusEl.textContent = "● Backend offline";
  }
}
 
form.addEventListener("submit", event => {
  event.preventDefault();
  ask(input.value);
});
document.querySelectorAll("[data-question]").forEach(button => {
  button.addEventListener("click", () => ask(button.dataset.question));
});
 
checkHealth();
setInterval(checkHealth, 30000);