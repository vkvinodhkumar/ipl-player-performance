(() => {
  if (window.__day31GuaranteedCsrf) return;
  window.__day31GuaranteedCsrf = true;
  const originalFetch = window.fetch.bind(window);
  async function tokenFromServer() {
    const r = await originalFetch("/api/csrf/", {
      method: "GET", credentials: "same-origin", headers: {"Accept": "application/json"}
    });
    if (!r.ok) throw new Error("CSRF bootstrap failed (HTTP " + r.status + ")");
    const data = await r.json();
    return data.csrfToken || "";
  }
  window.fetch = async function(input, init) {
    init = init || {};
    const method = String(init.method || (input instanceof Request ? input.method : "GET")).toUpperCase();
    const url = typeof input === "string" ? input : (input && input.url) || "";
    const sameOrigin = url.startsWith("/") || url.startsWith(window.location.origin);
    if (sameOrigin && ["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
      const token = await tokenFromServer();
      const headers = new Headers(init.headers || (input instanceof Request ? input.headers : undefined));
      if (!headers.has("X-CSRFToken")) headers.set("X-CSRFToken", token);
      init = Object.assign({}, init, {headers, credentials: "same-origin"});
    }
    return originalFetch(input, init);
  };
})();
