import { getStore } from "@netlify/blobs";
import type { Config, Context } from "@netlify/functions";

// ---------- Configuração do evento ----------
const PRICES: Record<string, number> = { adulto: 99.9, teen: 50, crianca: 0 };
const CAT_LABEL: Record<string, string> = {
  adulto: "Ingresso",
  teen: "11 a 15 anos",
  crianca: "Até 10 anos (não paga)",
};

const db = () => getStore({ name: "podium9anos", consistency: "strong" });
const files = () => getStore({ name: "podium9anos-comprovantes", consistency: "strong" });

// ---------- Utilidades ----------
const ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function rand(n: number) {
  const bytes = crypto.getRandomValues(new Uint8Array(n));
  let s = "";
  for (const b of bytes) s += ALPHA[b % ALPHA.length];
  return s;
}
const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
const bad = (msg: string, status = 400) => json({ error: msg }, status);
const round2 = (n: number) => Math.round(n * 100) / 100;
const clean = (s: unknown, max = 120) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, max);

type Role = "admin" | "victor" | "portaria";
function roleOf(req: Request): Role | null {
  const pin = req.headers.get("x-pin") || "";
  if (!pin) return null;
  if (pin === Netlify.env.get("VICTOR_PIN")) return "victor";
  if (pin === Netlify.env.get("ADMIN_PIN")) return "admin";
  if (pin === Netlify.env.get("PORTARIA_PIN")) return "portaria";
  return null;
}
const can = {
  admin: (r: Role | null) => r === "admin" || r === "victor",
  victor: (r: Role | null) => r === "victor",
  portaria: (r: Role | null) => r !== null,
};

function sanitizePeople(raw: unknown): { name: string; cat: string; price: number }[] | null {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > 20) return null;
  const out = [];
  for (const p of raw) {
    const name = clean(p?.name, 90);
    const cat = String(p?.cat || "");
    if (name.length < 3 || !(cat in PRICES)) return null;
    out.push({ name, cat, price: PRICES[cat] });
  }
  return out;
}

async function listJSON(prefix: string) {
  const store = db();
  const { blobs } = await store.list({ prefix });
  const items = await Promise.all(blobs.map((b) => store.get(b.key, { type: "json" })));
  return items.filter(Boolean) as any[];
}

async function issueTickets(order: any) {
  const store = db();
  if (order.tickets?.length) return order;
  order.tickets = [];
  for (const p of order.people) {
    const token = rand(14);
    const t = { token, orderId: order.id, name: p.name, cat: p.cat, checkedInAt: null };
    await store.setJSON(`tickets/${token}`, t);
    order.tickets.push({ token, name: p.name, cat: p.cat });
  }
  return order;
}

function publicOrder(o: any) {
  return {
    id: o.id,
    status: o.status,
    total: o.total,
    method: o.method,
    people: o.people,
    buyer: { name: o.buyer?.name },
    tickets: o.status === "pago" ? o.tickets || [] : [],
    createdAt: o.createdAt,
  };
}

// ---------- Handler ----------
export default async (req: Request, context: Context) => {
  const url = new URL(req.url);
  const route = url.pathname.replace(/^\/api\/?/, "");
  const method = req.method;
  const store = db();
  const role = roleOf(req);

  try {
    // ===== Público =====
    if (route === "order" && method === "POST") {
      const body = await req.json();
      const people = sanitizePeople(body.people);
      if (!people) return bad("Confira os nomes completos de cada pessoa.");
      const buyer = {
        name: clean(body.buyer?.name, 90),
        whatsapp: clean(body.buyer?.whatsapp, 30).replace(/[^\d+]/g, ""),
        email: clean(body.buyer?.email, 120).toLowerCase(),
      };
      if (buyer.name.length < 3) return bad("Informe seu nome completo.");
      if (buyer.whatsapp.replace(/\D/g, "").length < 10) return bad("Informe um WhatsApp com DDD.");
      const methodPay = body.method === "cartao" ? "cartao" : "pix";
      const total = round2(people.reduce((s, p) => s + p.price, 0));
      const order = {
        id: "P9" + rand(5),
        key: rand(16),
        createdAt: new Date().toISOString(),
        buyer,
        people,
        total,
        method: total === 0 ? "gratis" : methodPay,
        status: "pendente",
        source: "site",
        proof: null as null | string,
        paidAt: null,
        notes: "",
        tickets: [],
        sent: { whatsapp: false, email: false },
      };
      await store.setJSON(`orders/${order.id}`, order);
      return json({ id: order.id, key: order.key, total, people, method: order.method });
    }

    if (route === "proof" && method === "POST") {
      const id = url.searchParams.get("id") || "";
      const key = url.searchParams.get("k") || "";
      const order: any = await store.get(`orders/${id}`, { type: "json" });
      if (!order || order.key !== key) return bad("Pedido não encontrado.", 404);
      const form = await req.formData();
      const file = form.get("file") as File | null;
      if (!file) return bad("Arquivo não enviado.");
      if (file.size > 4 * 1024 * 1024) return bad("Arquivo muito grande (máx. 4 MB).");
      const type = file.type || "application/octet-stream";
      if (!/^image\/|application\/pdf/.test(type)) return bad("Envie imagem ou PDF.");
      await files().set(id, await file.arrayBuffer(), { metadata: { type, name: clean(file.name, 80) } });
      order.proof = type;
      order.proofAt = new Date().toISOString();
      await store.setJSON(`orders/${id}`, order);
      return json({ ok: true });
    }

    if (route === "status" && method === "GET") {
      const id = url.searchParams.get("id") || "";
      const key = url.searchParams.get("k") || "";
      const order: any = await store.get(`orders/${id}`, { type: "json" });
      if (!order || order.key !== key) return bad("Pedido não encontrado.", 404);
      return json(publicOrder(order));
    }

    if (route === "ticket" && method === "GET") {
      const token = (url.searchParams.get("t") || "").toUpperCase();
      if (!/^[A-Z0-9]{8,20}$/.test(token)) return bad("Ingresso inválido.", 404);
      const t: any = await store.get(`tickets/${token}`, { type: "json" });
      if (!t) return bad("Ingresso não encontrado.", 404);
      const order: any = await store.get(`orders/${t.orderId}`, { type: "json" });
      if (!order || order.status !== "pago") return bad("Ingresso não está ativo.", 404);
      return json({ token, name: t.name, cat: t.cat, catLabel: CAT_LABEL[t.cat], orderId: t.orderId, checkedIn: !!t.checkedInAt });
    }

    if (route === "whoami" && method === "GET") {
      if (!role) return bad("Senha incorreta.", 401);
      return json({ role, user: (req.headers.get("x-user") || "").trim().toLowerCase() });
    }

    // ===== Administração (Admin + Victor) =====
    if (route.startsWith("admin/")) {
      if (!can.admin(role)) return bad("PIN incorreto.", 401);
      const action = route.slice(6);

      if (action === "orders" && method === "GET") {
        const orders = await listJSON("orders/");
        const tickets = await listJSON("tickets/");
        const checked = new Set(tickets.filter((t) => t.checkedInAt).map((t) => t.token));
        for (const o of orders) {
          delete o.key;
          o.tickets = (o.tickets || []).map((t: any) => ({ ...t, checkedIn: checked.has(t.token) }));
        }
        orders.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
        return json({ orders });
      }

      if (action === "proof" && method === "GET") {
        const id = url.searchParams.get("id") || "";
        const entry = await files().getWithMetadata(id, { type: "arrayBuffer" });
        if (entry === null) return bad("Sem comprovante.", 404);
        return new Response(entry.data as ArrayBuffer, {
          headers: { "content-type": String(entry.metadata?.type || "application/octet-stream"), "cache-control": "no-store" },
        });
      }

      if (method === "POST") {
        const body = await req.json();
        const id = clean(body.id, 20);
        const order: any = await store.get(`orders/${id}`, { type: "json" });
        if (!order) return bad("Pedido não encontrado.", 404);

        if (action === "confirm") {
          order.status = "pago";
          order.paidAt = order.paidAt || new Date().toISOString();
          if (body.method) order.method = clean(body.method, 20);
          await issueTickets(order);
        } else if (action === "pending") {
          order.status = "pendente";
        } else if (action === "cancel") {
          order.status = "cancelado";
        } else if (action === "sent") {
          order.sent = { ...(order.sent || {}), [body.channel === "email" ? "email" : "whatsapp"]: true };
        } else if (action === "note") {
          order.notes = clean(body.notes, 500);
        } else if (action === "delete") {
          for (const t of order.tickets || []) await store.delete(`tickets/${t.token}`);
          await store.delete(`orders/${id}`);
          await files().delete(id);
          return json({ ok: true, deleted: id });
        } else return bad("Ação desconhecida.");

        await store.setJSON(`orders/${id}`, order);
        delete order.key;
        return json({ order });
      }
    }

    // ===== Caixa do Victor =====
    if (route.startsWith("caixa/")) {
      const user = (req.headers.get("x-user") || "").trim().toLowerCase();
      if (!can.victor(role) || user !== "victor") return bad("Usuário ou senha incorretos.", 401);
      const action = route.slice(6);

      if (action === "summary" && method === "GET") {
        const orders = await listJSON("orders/");
        const expenses = await listJSON("expenses/");
        expenses.sort((a, b) => (b.date + b.createdAt).localeCompare(a.date + a.createdAt));
        const paid = orders.filter((o) => o.status === "pago");
        const sum = (arr: any[], f: (x: any) => number) => round2(arr.reduce((s, x) => s + f(x), 0));
        const byMethod: Record<string, number> = {};
        for (const o of paid) byMethod[o.method] = round2((byMethod[o.method] || 0) + o.total);
        const byCat: Record<string, number> = {};
        for (const e of expenses) byCat[e.category] = round2((byCat[e.category] || 0) + e.amount);
        const people = { adulto: 0, teen: 0, crianca: 0 };
        for (const o of paid) for (const p of o.people) (people as any)[p.cat]++;
        const pending = orders.filter((o) => o.status === "pendente");
        const cashSales = orders
          .filter((o) => o.source === "caixa" && o.status !== "cancelado")
          .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
          .map((o) => ({ id: o.id, createdAt: o.createdAt, buyer: o.buyer, people: o.people, total: o.total, method: o.method, tickets: o.tickets, sent: o.sent }));
        return json({
          income: sum(paid, (o) => o.total),
          expensesTotal: sum(expenses, (e) => e.amount),
          pendingTotal: sum(pending, (o) => o.total),
          pendingCount: pending.length,
          byMethod,
          byCat,
          people,
          expenses,
          cashSales,
        });
      }

      if (action === "sale" && method === "POST") {
        const body = await req.json();
        const people = sanitizePeople(body.people);
        if (!people) return bad("Confira os nomes completos de cada pessoa.");
        const total = body.total != null && body.total !== "" ? round2(Number(body.total)) : round2(people.reduce((s, p) => s + p.price, 0));
        if (!(total >= 0)) return bad("Valor inválido.");
        const order: any = {
          id: "P9" + rand(5),
          key: rand(16),
          createdAt: new Date().toISOString(),
          buyer: {
            name: clean(body.buyer?.name || people[0].name, 90),
            whatsapp: clean(body.buyer?.whatsapp, 30).replace(/[^\d+]/g, ""),
            email: clean(body.buyer?.email, 120).toLowerCase(),
          },
          people,
          total,
          method: ["dinheiro", "pix", "cartao"].includes(body.method) ? body.method : "dinheiro",
          status: "pago",
          source: "caixa",
          proof: null,
          paidAt: new Date().toISOString(),
          notes: clean(body.notes, 300),
          tickets: [],
          sent: { whatsapp: false, email: false },
        };
        await issueTickets(order);
        await store.setJSON(`orders/${order.id}`, order);
        return json({ order });
      }

      if (action === "expense" && method === "POST") {
        const body = await req.json();
        const amount = round2(Number(String(body.amount).replace(",", ".")));
        if (!(amount > 0)) return bad("Informe o valor.");
        const e = {
          id: "D" + rand(6),
          createdAt: new Date().toISOString(),
          date: /^\d{4}-\d{2}-\d{2}$/.test(body.date) ? body.date : new Date().toISOString().slice(0, 10),
          category: clean(body.category, 30) || "Outros",
          desc: clean(body.desc, 200),
          amount,
          method: clean(body.method, 20),
        };
        await store.setJSON(`expenses/${e.id}`, e);
        return json({ expense: e });
      }

      if (action === "expense-delete" && method === "POST") {
        const body = await req.json();
        await store.delete(`expenses/${clean(body.id, 20)}`);
        return json({ ok: true });
      }

      if (action === "sale-cancel" && method === "POST") {
        const body = await req.json();
        const order: any = await store.get(`orders/${clean(body.id, 20)}`, { type: "json" });
        if (!order || order.source !== "caixa") return bad("Venda não encontrada.", 404);
        order.status = "cancelado";
        await store.setJSON(`orders/${order.id}`, order);
        return json({ ok: true });
      }
    }

    // ===== Portaria =====
    if (route.startsWith("portaria/")) {
      if (!can.portaria(role)) return bad("PIN incorreto.", 401);
      const action = route.slice(9);

      if (action === "checkin" && method === "POST") {
        const body = await req.json();
        let token = String(body.token || "").trim();
        const m = token.match(/[?&]t=([A-Za-z0-9]+)/);
        if (m) token = m[1];
        token = token.toUpperCase();
        if (!/^[A-Z0-9]{8,20}$/.test(token)) return json({ result: "invalido" });
        const t: any = await store.get(`tickets/${token}`, { type: "json" });
        if (!t) return json({ result: "invalido" });
        const order: any = await store.get(`orders/${t.orderId}`, { type: "json" });
        if (!order || order.status !== "pago") return json({ result: "inativo", name: t.name, catLabel: CAT_LABEL[t.cat] });
        if (t.checkedInAt && !body.force) {
          return json({ result: "repetido", name: t.name, catLabel: CAT_LABEL[t.cat], cat: t.cat, checkedInAt: t.checkedInAt, token });
        }
        t.checkedInAt = new Date().toISOString();
        await store.setJSON(`tickets/${token}`, t);
        return json({ result: "ok", name: t.name, catLabel: CAT_LABEL[t.cat], cat: t.cat, checkedInAt: t.checkedInAt, token });
      }

      if (action === "undo" && method === "POST") {
        const body = await req.json();
        const token = clean(body.token, 20).toUpperCase();
        const t: any = await store.get(`tickets/${token}`, { type: "json" });
        if (!t) return bad("Ingresso não encontrado.", 404);
        t.checkedInAt = null;
        await store.setJSON(`tickets/${token}`, t);
        return json({ ok: true });
      }

      if (action === "list" && method === "GET") {
        const orders = (await listJSON("orders/")).filter((o) => o.status === "pago");
        const tickets = await listJSON("tickets/");
        const byToken = new Map(tickets.map((t) => [t.token, t]));
        const list = [];
        for (const o of orders)
          for (const tk of o.tickets || []) {
            const t = byToken.get(tk.token);
            if (t) list.push({ token: t.token, name: t.name, cat: t.cat, catLabel: CAT_LABEL[t.cat], orderId: o.id, checkedInAt: t.checkedInAt });
          }
        list.sort((a, b) => a.name.localeCompare(b.name, "pt-BR"));
        return json({ list });
      }
    }

    return bad("Rota não encontrada.", 404);
  } catch (err: any) {
    console.error(err);
    return bad("Erro no servidor: " + (err?.message || "desconhecido"), 500);
  }
};

export const config: Config = { path: "/api/*" };
