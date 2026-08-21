const algorithms = [
  ["caesar", "Caesar Cipher"],
  ["vigenere", "Vigenère Cipher"],
  ["atbash", "Atbash Cipher"],
  ["rot13", "ROT13"]
];

const $ = id => document.getElementById(id);
const status = document.createElement("div");
status.className = "toast";
document.body.appendChild(status);

function setupSelect(id) {
  $(id).innerHTML = algorithms.map(([v,n]) => `<option value="${v}">${n}</option>`).join("");
}
setupSelect("encAlgorithm");
setupSelect("decAlgorithm");

function updateKeyVisibility(selectId, wrapId) {
  const needsKey = ["caesar", "vigenere"].includes($(selectId).value);
  $(wrapId).style.display = needsKey ? "block" : "none";
}
$("encAlgorithm").addEventListener("change", () => updateKeyVisibility("encAlgorithm", "encKeyWrap"));
$("decAlgorithm").addEventListener("change", () => updateKeyVisibility("decAlgorithm", "decKeyWrap"));
updateKeyVisibility("encAlgorithm", "encKeyWrap");
updateKeyVisibility("decAlgorithm", "decKeyWrap");

function toast(msg, error=false) {
  status.textContent = msg;
  status.className = "toast show" + (error ? " error" : "");
  setTimeout(() => status.classList.remove("show"), 2500);
}

async function api(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}

async function processBox(type) {
  const enc = type === "encrypt";
  const message = $(enc ? "encMessage" : "decMessage").value;
  const algorithm = $(enc ? "encAlgorithm" : "decAlgorithm").value;
  const key = $(enc ? "encKey" : "decKey").value;

  if (!message.trim()) return toast("Enter a message first.", true);

  try {
    const data = await api(`/api/${type}`, {message, algorithm, key});
    $(enc ? "encOutput" : "decOutput").textContent = data.result;
    $(enc ? "encHash" : "decHash").textContent = data.integrity_hash;
    toast(`${enc ? "Encryption" : "Decryption"} completed successfully.`);
    if (enc) $("decMessage").value = data.result;
  } catch (e) { toast(e.message, true); }
}

$("encryptBtn").addEventListener("click", () => processBox("encrypt"));
$("decryptBtn").addEventListener("click", () => processBox("decrypt"));

$("attackBtn").addEventListener("click", async () => {
  const message = $("attackMessage").value;
  if (!message.trim()) return toast("Paste Caesar ciphertext first.", true);
  try {
    const data = await api("/api/attack", {message, algorithm: "caesar"});
    $("attackResults").innerHTML = data.candidates.map((x, i) =>
      `<div class="candidate ${i === 0 && x.score > 0 ? "best" : ""}">
        <span>Key <b>${x.key}</b></span><code>${escapeHtml(x.text)}</code><small>score ${x.score}</small>
      </div>`).join("");
    toast("Brute-force analysis completed.");
  } catch (e) { toast(e.message, true); }
});

$("hashBtn").addEventListener("click", async () => {
  const message = $("hashMessage").value;
  if (!message.trim()) return toast("Enter a message first.", true);
  try {
    const data = await api("/api/hash", {message});
    $("hashOutput").textContent = data.sha256;
    toast("SHA-256 generated.");
  } catch (e) { toast(e.message, true); }
});

document.querySelectorAll("[data-copy]").forEach(btn => {
  btn.addEventListener("click", async () => {
    const text = $(btn.dataset.copy).textContent;
    if (!text || text.includes("will appear")) return;
    await navigator.clipboard.writeText(text);
    toast("Copied to clipboard.");
  });
});

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
