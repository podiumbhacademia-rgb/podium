// ===== Configuração do evento (edite aqui se algo mudar) =====
window.EVENT = {
  name: "9 Anos de Podium",
  subtitle: "Confraternização de fim de ano",
  dateISO: "2026-12-13T14:00:00-03:00",
  dateLabel: "Domingo, 13 de dezembro · 14h",
  address: "Rua Guimarânia, 221 · Boa Vista · BH",
  mapsURL: "https://www.google.com/maps/search/?api=1&query=Rua+Guimar%C3%A2nia+221+Boa+Vista+Belo+Horizonte",
  contactWa: "5531996221198",
  contactLabel: "(31) 99622-1198",
  site: "https://podium9anos.netlify.app",
  prices: { adulto: 99.9, teen: 50, crianca: 0 },
  catLabel: { adulto: "Ingresso", teen: "11 a 15 anos", crianca: "Até 10 anos (não paga)" },
  catShort: { adulto: "Inteira", teen: "11 a 15 anos", crianca: "Até 10 anos" },
  pix: {
    key: "podiumacademiabh@gmail.com",
    name: "VICTOR DA SILVA FERREIRA",
    city: "BELO HORIZONTE",
  },
  cardLinks: {
    adulto: "https://link.infinitepay.io/victor-silva-88b/VC1D-KFQvl1o2tQ-99,90",
    teen: "https://link.infinitepay.io/victor-silva-88b/VC1D-fLLtUq1MN4-50,00",
  },
};

// ===== Utilidades =====
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const brl = (n) => (n || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmtDT = (iso) => (iso ? new Date(iso).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }) : "");

function toast(msg) {
  let t = $(".toast");
  if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
  t.textContent = msg; t.classList.add("show");
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 2600);
}
async function copy(text, msg = "Copiado!") {
  try { await navigator.clipboard.writeText(text); }
  catch { const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); }
  toast(msg);
}

// ===== API =====
async function api(path, { method = "GET", body, pin, form } = {}) {
  const headers = {};
  if (pin) headers["x-pin"] = pin;
  let payload;
  if (form) payload = form;
  else if (body !== undefined) { headers["content-type"] = "application/json"; payload = JSON.stringify(body); }
  const res = await fetch("/api/" + path, { method, headers, body: payload });
  let data = {};
  try { data = await res.json(); } catch {}
  if (!res.ok) throw Object.assign(new Error(data.error || "Erro " + res.status), { status: res.status });
  return data;
}

// ===== QR Code (SVG) =====
function qrSVG(text, { ecc = "M", color = "#131210", bg = "#ffffff", margin = 2 } = {}) {
  const qr = qrcode(0, ecc); qr.addData(text); qr.make();
  const n = qr.getModuleCount(), size = n + margin * 2;
  let d = "";
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (qr.isDark(r, c)) d += `M${c + margin} ${r + margin}h1v1h-1z`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges"><rect width="${size}" height="${size}" fill="${bg}"/><path d="${d}" fill="${color}"/></svg>`;
}

// ===== Pix "copia e cola" (BR Code estático, padrão Banco Central) =====
function crc16(str) {
  let crc = 0xffff;
  for (let i = 0; i < str.length; i++) {
    crc ^= str.charCodeAt(i) << 8;
    for (let j = 0; j < 8; j++) crc = crc & 0x8000 ? ((crc << 1) ^ 0x1021) & 0xffff : (crc << 1) & 0xffff;
  }
  return crc.toString(16).toUpperCase().padStart(4, "0");
}
const tlv = (id, v) => id + String(v.length).padStart(2, "0") + v;
const plain = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9 .\-@]/g, "");
function pixPayload({ key, name, city, amount, txid = "***", desc = "" }) {
  const mai = tlv("00", "BR.GOV.BCB.PIX") + tlv("01", key) + (desc ? tlv("02", plain(desc).slice(0, 40)) : "");
  let p = tlv("00", "01") + tlv("26", mai) + tlv("52", "0000") + tlv("53", "986");
  if (amount > 0) p += tlv("54", amount.toFixed(2));
  p += tlv("58", "BR") + tlv("59", plain(name).toUpperCase().slice(0, 25)) + tlv("60", plain(city).toUpperCase().slice(0, 15));
  p += tlv("62", tlv("05", (txid || "***").replace(/[^A-Za-z0-9]/g, "").slice(0, 25) || "***"));
  p += "6304";
  return p + crc16(p);
}

// ===== Links de ingresso / mensagens =====
const ticketURL = (token) => `${EVENT.site}/i/?t=${token}`;
function waNumber(raw) {
  let d = String(raw || "").replace(/\D/g, "");
  if (!d) return "";
  if (d.length <= 11) d = "55" + d;
  return d;
}
function ticketMessage(order) {
  const first = (order.buyer?.name || "").split(" ")[0];
  const lines = (order.tickets || []).map((t) => `• ${t.name}: ${ticketURL(t.token)}`).join("\n");
  return `Oi, ${first}! Pagamento confirmado!\n\nSeus ingressos para a festa *9 Anos de Podium* (${EVENT.dateLabel}, ${EVENT.address}) estão aqui. Cada pessoa tem o próprio QR Code. É só abrir o link e mostrar na portaria:\n\n${lines}\n\nPedido ${order.id}. Te esperamos!`;
}
function waLink(order) {
  return `https://wa.me/${waNumber(order.buyer?.whatsapp)}?text=${encodeURIComponent(ticketMessage(order))}`;
}
function mailLink(order) {
  const subject = `Seus ingressos | 9 Anos de Podium (pedido ${order.id})`;
  return `mailto:${order.buyer?.email || ""}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(ticketMessage(order).replace(/\*/g, ""))}`;
}

// ===== Login por PIN dos painéis =====
async function pinGate(storageKey, onReady) {
  const gate = $("#gate"), app = $("#app");
  const tryPin = async (pin, silent) => {
    try {
      const { role } = await api("whoami", { pin });
      try { localStorage.setItem(storageKey, pin); } catch {}
      gate.classList.add("hide"); app.classList.remove("hide");
      onReady(pin, role);
    } catch (e) {
      try { localStorage.removeItem(storageKey); } catch {}
      if (!silent) toast(e.message || "PIN incorreto");
      gate.classList.remove("hide");
    }
  };
  let saved = null; try { saved = localStorage.getItem(storageKey); } catch {}
  if (saved) await tryPin(saved, true); else gate.classList.remove("hide");
  $("#gateForm").addEventListener("submit", (e) => { e.preventDefault(); tryPin($("#pinInput").value.trim()); });
  $$("[data-logout]").forEach((b) => b.addEventListener("click", () => { try { localStorage.removeItem(storageKey); } catch {} location.reload(); }));
}
