/**
 * Optional proxy in front of the Google Apps Script booking backend.
 * Apps Script cannot see the visitor's IP address, so this Worker:
 *   - rate-limits writes per IP (brief 2.4), using Cloudflare's rate limiting binding;
 *   - adds the IP to the request (signed with PROXY_SECRET) for the Meta Conversions API.
 * Secrets / vars: APPS_SCRIPT_URL (the /exec URL), PROXY_SECRET (same value as the Script Property),
 * ALLOWED_ORIGIN (e.g. https://a1esmat.com). Binding: LIMITER (see wrangler.toml).
 */
export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "https://a1esmat.com",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin",
    };
    const reply = (body, status = 200) =>
      new Response(typeof body === "string" ? body : JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json; charset=utf-8" } });

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const target = new URL(env.APPS_SCRIPT_URL);

    const ip = request.headers.get("CF-Connecting-IP") || "";
    if (request.method === "GET") {
      if (env.LIMITER) {
        const { success } = await env.LIMITER.limit({ key: "get:" + (ip || "unknown") });
        if (!success) return reply({ ok: false, error: "rate_limited" }, 429);
      }
      new URL(request.url).searchParams.forEach((v, k) => target.searchParams.set(k, v));
      const r = await fetch(target, { redirect: "follow" });
      return reply(await r.text(), r.status);
    }
    if (request.method !== "POST") return reply({ ok: false, error: "method_not_allowed" }, 405);

    if (env.LIMITER) {
      const { success } = await env.LIMITER.limit({ key: ip || "unknown" });
      if (!success) return reply({ ok: false, error: "rate_limited" }, 429);
    }
    let data;
    try { data = await request.json(); } catch (e) { return reply({ ok: false, error: "invalid_json" }, 400); }
    if (!data || typeof data !== "object" || Array.isArray(data)) return reply({ ok: false, error: "invalid_json" }, 400);
    data.client_ip = ip;
    data.proxy_secret = env.PROXY_SECRET;
    const r = await fetch(target, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data), redirect: "follow" });
    return reply(await r.text(), r.status);
  },
};
