// Local reverse proxy: Chrome → http://127.0.0.1:8787 → (Node fetch via HTTPS_PROXY) → builder.craftons.com.au
import http from 'node:http';
const ORIGIN = process.env.RPROXY_ORIGIN || 'https://builder.craftons.com.au';
const HOP = new Set(['host','connection','content-length','content-encoding','transfer-encoding','accept-encoding']);
http.createServer(async (req, res) => {
  try {
    const chunks = []; for await (const c of req) chunks.push(c);
    const body = chunks.length ? Buffer.concat(chunks) : undefined;
    const h = {}; for (const [k, v] of Object.entries(req.headers)) if (!HOP.has(k.toLowerCase())) h[k] = v;
    h['accept-encoding'] = 'identity'; h['origin'] = ORIGIN; h['referer'] = ORIGIN + '/';
    const r = await fetch(ORIGIN + req.url, { method: req.method, headers: h, body, redirect: 'manual' });
    const out = {}; r.headers.forEach((v, k) => { if (!HOP.has(k) && k !== 'content-security-policy' && k !== 'strict-transport-security') out[k] = v; });
    if (out['location']) out['location'] = out['location'].replace(ORIGIN, 'http://127.0.0.1:8787');
    const buf = Buffer.from(await r.arrayBuffer());
    const ct = out['content-type'] || '';
    let data = buf;
    if (/text\/html|javascript|json|css/.test(ct)) data = Buffer.from(buf.toString('utf8').split(ORIGIN).join('http://127.0.0.1:8787'));
    res.writeHead(r.status, out); res.end(data);
  } catch (e) { res.writeHead(502); res.end('rproxy: ' + e.message); }
}).listen(8787, '127.0.0.1', () => console.log('rproxy on 8787'));
