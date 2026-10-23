(() => {
const $ = id => document.getElementById(id);
const show = (id, value) => { $(id).textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2); };
async function requestJson(url, options = {}) {
  const response = await fetch(url, {headers: {"Accept":"application/json", ...(options.headers || {})}, ...options});
  const raw = await response.text();
  let data; try { data = raw ? JSON.parse(raw) : {}; } catch { throw new Error(`HTTP ${response.status}: response was not JSON: ${raw.slice(0,200)}`); }
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
  return data;
}
async function postForm(endpointId, payloadId, resultId) {
  const endpoint = $(endpointId).value.trim();
  if (!endpoint) { show(resultId, "Select an endpoint only after confirming it is registered in Django URLs."); return; }
  let payload; try { payload = JSON.parse($(payloadId).value); } catch(e) { show(resultId, `Invalid JSON: ${e.message}`); return; }
  show(resultId, "Requesting…");
  try { show(resultId, await requestJson(endpoint, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)})); }
  catch(e) { show(resultId, e.message); }
}
$("runPrediction").addEventListener("click", () => postForm("predictionEndpoint","predictionPayload","predictionResult"));
$("runBatch").addEventListener("click", () => postForm("batchEndpoint","batchPayload","batchResult"));
$("loadMetrics").addEventListener("click", async () => {
  const endpoint = $("metricsEndpoint").value.trim(); if (!endpoint) { show("metricsResult","Enter a registered metrics endpoint."); return; }
  show("metricsResult","Loading…");
  try { show("metricsResult", await requestJson(endpoint)); }
  catch(e) { show("metricsResult", `${e.message}
No metrics were fabricated. Check URL configuration or expose saved reports through a read-only API.`); }
});
(async () => { try { const d = await requestJson("/api/eda/summary/"); $("status").className="alert alert-success"; $("status").textContent="Summary API reachable: "+JSON.stringify(d); }
catch(e) { $("status").className="alert alert-warning"; $("status").textContent="Summary API check failed: "+e.message; } })();
})();