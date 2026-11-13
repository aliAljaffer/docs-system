const IMAGE = /\.(?:jpe?g|png|webp)$/i;
const PREFIX = "docs";

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (!IMAGE.test(url.pathname)) {
      return env.ASSETS.fetch(request);
    }

    const cache = caches.default;
    const cacheKey = new Request(url.origin + url.pathname);
    const isCacheable = request.method === "GET";

    if (isCacheable) {
      const hit = await cache.match(cacheKey);
      if (hit) return hit;
    }

    const object = await env.BUCKET.get(PREFIX + url.pathname);
    if (!object) return env.ASSETS.fetch(request);

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("ETag", object.httpEtag);
    headers.set("Cache-Control", "public, max-age=604800");
    headers.set("X-Content-Type-Options", "nosniff");

    const response = new Response(isCacheable ? object.body : null, { headers });
    if (isCacheable) ctx.waitUntil(cache.put(cacheKey, response.clone()));
    return response;
  },
};
