
(function day31InstallCsrfFetch() {
  if (window.__day31CsrfFetchInstalled) return;
  window.__day31CsrfFetchInstalled = true;
  const originalFetch = window.fetch.bind(window);
  window.fetch = function(input, init) {
    init = init || {};
    const method = String(init.method || "GET").toUpperCase();
    const url = typeof input === "string" ? input : (input && input.url) || "";
    if (method === "POST" && (url.startsWith("/") || url.startsWith(window.location.origin))) {
      const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
      const token = match ? decodeURIComponent(match[1]) : "";
      const headers = new Headers(init.headers || (input instanceof Request ? input.headers : undefined));
      if (token && !headers.has("X-CSRFToken")) headers.set("X-CSRFToken", token);
      init = Object.assign({}, init, {headers: headers, credentials: init.credentials || "same-origin"});
    }
    return originalFetch(input, init);
  };
})();

(() => {
const ROUTES = {"batting": {"fragment": "predict/batting/", "url": "/api/predict/batting/", "label": "Batting Prediction", "description": "Estimate next-match runs.", "registered": true}, "bowling": {"fragment": "predict/bowling/", "url": "/api/predict/bowling/", "label": "Bowling Prediction", "description": "Estimate wickets and runs conceded.", "registered": true}, "batch": {"fragment": "predict/batch/", "url": "/api/predict/batch/", "label": "Batch Prediction", "description": "Submit multiple player records.", "registered": true}, "batch_alt": {"fragment": "batch/predict/", "url": "/api/batch/predict/", "label": "Batch Prediction", "description": "Alternate batch route.", "registered": false}, "unified": {"fragment": "predict/", "url": "/api/predict/", "label": "Unified Prediction API", "description": "Use the endpoint's documented schema.", "registered": true}, "summary": {"fragment": "eda/summary/", "url": "/api/eda/summary/", "label": "EDA Summary", "description": "Historical dataset summary.", "registered": true}, "batting_eda": {"fragment": "eda/batting/", "url": "/api/eda/batting/", "label": "Batting EDA", "description": "Batting analytics.", "registered": true}, "bowling_eda": {"fragment": "eda/bowling/", "url": "/api/eda/bowling/", "label": "Bowling EDA", "description": "Bowling analytics.", "registered": true}, "recent": {"fragment": "eda/recent-form/", "url": "/api/eda/recent-form/", "label": "Recent Form", "description": "Recent player performance.", "registered": true}};
const $ = id => document.getElementById(id);
const show = (id, v) => { $(id).textContent = typeof v === "string" ? v : JSON.stringify(v, null, 2); };
Object.values(ROUTES).forEach(route => {
  const col = document.createElement("div"); col.className = "col";
  const card = document.createElement("div"); card.className = "endpoint-card h-100";
  const title = document.createElement("strong"); title.textContent = route.label;
  const desc = document.createElement("p"); desc.className = "small text-secondary mt-2"; desc.textContent = route.description;
  const status = document.createElement("span"); status.className = route.registered ? "badge text-bg-success" : "badge text-bg-secondary";
  status.textContent = route.registered ? "Registered" : "Not registered";
  card.append(title, desc, status);
  if (route.registered) { const a = document.createElement("a"); a.href = route.url; a.className = "d-block mt-2"; a.textContent = "Open API endpoint"; card.append(a); }
  col.append(card); $("endpointCards").append(col);
});
function fill(id, keys, emptyLabel) {
  const select = $(id); select.innerHTML = "";
  const first = document.createElement("option"); first.value = ""; first.textContent = emptyLabel; select.append(first);
  keys.filter(k => ROUTES[k] && ROUTES[k].registered).forEach(k => {
    const o = document.createElement("option"); o.value = ROUTES[k].url; o.textContent = ROUTES[k].label + " — " + ROUTES[k].url; select.append(o);
  });
  if (select.options.length === 1) select.disabled = true;
}
fill("singleEndpoint", ["batting","bowling","unified"], "No registered prediction endpoint found");
fill("batchEndpoint", ["batch","batch_alt"], "No registered batch endpoint found");
async function req(url, options={}) {
  const r = await fetch(url, {headers: {"Accept":"application/json", ...(options.headers||{})}, ...options});
  const t = await r.text(); let data;
  try { data = t ? JSON.parse(t) : {}; } catch { throw new Error("HTTP " + r.status + ": response was not JSON: " + t.slice(0,250)); }
  if (!r.ok) throw new Error("HTTP " + r.status + ": " + JSON.stringify(data));
  return data;
}
async function post(endpointId, payloadId, resultId) {
  const url = $(endpointId).value;
  if (!url) { show(resultId, "No registered endpoint selected. Inspect ipl_api/urls.py."); return; }
  let payload; try { payload = JSON.parse($(payloadId).value); } catch(e) { show(resultId, "Invalid JSON: " + e.message); return; }
  show(resultId, "Requesting…");
  try { show(resultId, await req(url, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)})); }
  catch(e) { show(resultId, e.message); }
}
$("runSingle").addEventListener("click", () => post("singleEndpoint","singlePayload","singleResult"));
$("runPlayerPrediction").addEventListener("click", async () => {
  const player_name = $("playerName").value.trim();
  const target = $("playerTarget").value;
  if (!player_name) { show("playerPredictionResult", "Enter a player name first."); return; }
  show("playerPredictionResult", "Requesting prediction…");
  try {
    const result = await req("/api/predict/player/", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({player_name, target})
    });
    show("playerPredictionResult", result);
  } catch (e) { show("playerPredictionResult", e.message); }
});

$("runBatch").addEventListener("click", () => post("batchEndpoint","batchPayload","batchResult"));
$("loadMetrics").addEventListener("click", async () => {
  show("metricsResult","Loading…");
  try { show("metricsResult", await req($("metricsUrl").value.trim())); }
  catch(e) { show("metricsResult", e.message + "\nIf this route is not registered, compare reports/day10, day12, day13 and day14."); }
});
})();