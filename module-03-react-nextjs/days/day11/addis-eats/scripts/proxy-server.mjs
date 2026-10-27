/**
 * @file scripts/proxy-server.mjs
 * @description A minimal Node.js HTTP proxy that forwards API requests to
 * the Next.js dev server. Useful when testing the app behind a corporate
 * proxy or from a different port.
 *
 * Usage:
 *   node scripts/proxy-server.mjs
 *
 * The proxy listens on PORT (default 3001) and forwards everything to
 * NEXT_PORT (default 3000).
 *
 * This is a DEVELOPMENT-ONLY helper — do not use in production.
 */

import http from "http";

const PORT      = process.env.PORT      ?? 3001;
const NEXT_PORT = process.env.NEXT_PORT ?? 3000;
const NEXT_HOST = "localhost";

const server = http.createServer((clientReq, clientRes) => {
  const options = {
    hostname: NEXT_HOST,
    port:     NEXT_PORT,
    path:     clientReq.url,
    method:   clientReq.method,
    headers:  clientReq.headers,
  };

  const proxyReq = http.request(options, (proxyRes) => {
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes, { end: true });
  });

  proxyReq.on("error", (err) => {
    console.error("[proxy] upstream error:", err.message);
    clientRes.writeHead(502);
    clientRes.end("Bad Gateway — Next.js dev server may not be running.");
  });

  clientReq.pipe(proxyReq, { end: true });
});

server.listen(PORT, () => {
  console.log(`[proxy] Listening on http://localhost:${PORT}`);
  console.log(`[proxy] Forwarding to http://${NEXT_HOST}:${NEXT_PORT}`);
});
