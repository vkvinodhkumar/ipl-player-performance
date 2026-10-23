(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const jsonText = value => JSON.stringify(value, null, 2);
  const show = (id, value) => { const el = $(id); if (el) el.textContent = typeof value === "string" ? value : jsonText(value); };
  const safeParse = (raw, label) => {
    try { return JSON.parse(raw); }
    catch (err) { throw new Error(label + " is not valid JSON: " + err.message); }
  };
  async function request(url, options = {}) {
    const response = await fetch(url, {
      credentials: "same-origin",
      headers: { "Accept": "application/json", ...(options.body ? {"Content-Type":"application/json"} : {}), ...(options.headers || {}) },
      ...options
    });
    const raw = await response.text();
    let body;
    try { body = raw ? JSON.parse(raw) : null; } catch { body = raw; }
    if (!response.ok) {
      const detail = body && typeof body === "object" ? (body.detail || body.error || body.message || body) : body;
      throw new Error("HTTP " + response.status + " from " + url + ": " + (typeof detail === "string" ? detail : jsonText(detail)));
    }
    return body;
  }
  function showLoading(id, message) {
    const el = $(id);
    if (!el) return;
    el.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span><span></span>';
    const text = el.querySelector("span:last-child");
    if (text) text.textContent = message;
    el.setAttribute("aria-live", "polite");
  }
  function setMessage(message, kind = "secondary") {
    const el = $("globalMessage");
    if (el) { el.className = "alert alert-" + kind; el.textContent = message; }
  }
  document.querySelectorAll("#sectionTabs [data-target]").forEach(button => {
    button.addEventListener("click", () => {
      document.querySelectorAll("#sectionTabs .nav-link").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".feature-section").forEach(s => s.classList.remove("active"));
      button.classList.add("active");
      $(button.dataset.target).classList.add("active");
    });
  });

  async function loadOverview() {
    try {
      const data = await request("/api/eda/summary/");
      const obj = data && data.results ? data.results : data;
      const aliases = {
        playersMetric: ["players", "player_count", "total_players"],
        matchesMetric: ["matches", "match_count", "total_matches"],
        battingMetric: ["batting_records", "batting_count"],
        bowlingMetric: ["bowling_records", "bowling_count"]
      };
      for (const [id, keys] of Object.entries(aliases)) {
        const key = keys.find(k => obj && obj[k] !== undefined);
        $(id).textContent = key ? obj[key] : "—";
      }
      setMessage("Summary API reachable. Counts reflect the response fields available from the backend.", "success");
    } catch (err) { setMessage("Summary API error: " + err.message, "danger"); }
  }
  $("refreshOverview").addEventListener("click", loadOverview);
  loadOverview();

  $("searchPlayer").addEventListener("click", async () => {
    const name = $("playerName").value.trim();
    if (!name) { show("playerResult", "Enter a player name."); return; }
    try { show("playerResult", await request("/api/players/" + encodeURIComponent(name) + "/")); }
    catch (err) { show("playerResult", err.message); }
  });

  // Populate player suggestions only if the configured endpoint supports this GET contract.
  (async () => {
    try {
      const data = await request("/api/players/search-options/");
      const rows = Array.isArray(data) ? data : (data.results || data.players || []);
      for (const row of rows) {
        const value = typeof row === "string" ? row : (row.player_name || row.name);
        if (value) { const option = document.createElement("option"); option.value = value; $("playerOptions").appendChild(option); }
      }
    } catch (err) { console.info("Player suggestions not available:", err.message); }
  })();

  async function prediction(endpoint, playerId, jsonId, resultId) {
    const player = $(playerId).value.trim();
    const raw = $(jsonId).value.trim();
    try {
      let payload;
      if (raw) payload = safeParse(raw, "Feature payload");
      else if (player) {
        const target = endpoint.includes("batting") ? "next_match_runs" :
          (endpoint.includes("bowling") ? "next_match_wickets" : "");
        if (!target) throw new Error("Select a supported target.");
        payload = {player_name: player, target: target};
        show(resultId, await request("/api/predict/player/", {method:"POST", body:JSON.stringify(payload)}));
        return;
      } else throw new Error("Enter a player name or provide feature JSON.");
      show(resultId, await request(endpoint, {method:"POST", body:JSON.stringify(payload)}));
    } catch (err) { show(resultId, err.message); }
  }
  $("runBattingML").addEventListener("click", () => prediction("/api/predict/batting/", "battingPlayer", "battingJson", "battingMLResult"));
  $("runBowlingML").addEventListener("click", () => prediction("/api/predict/bowling/", "bowlingPlayer", "bowlingJson", "bowlingMLResult"));

  $("loadMetrics").addEventListener("click", async () => {
    try { show("metricsResult", await request("/api/eda/model-metrics/")); }
    catch (err) { show("metricsResult", "Saved metrics could not be loaded: " + err.message); }
  });
  $("loadEDA").addEventListener("click", async () => {
    try { show("edaResult", await request($("edaEndpoint").value)); }
    catch (err) { show("edaResult", err.message); }
  });
  $("runBatch").addEventListener("click", async () => {
    try {
      const payload = safeParse($("batchJson").value, "Batch payload");
      const data = await request($("batchEndpoint").value, {method:"POST", body:JSON.stringify(payload)});
      show("batchResult", data);
      const exportButton = document.getElementById("downloadBatch");
      if (exportButton) exportButton.onclick = () => {
        const blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a"); a.href=url; a.download="ipl_batch_results.json"; a.click();
        URL.revokeObjectURL(url);
      };
      if (exportButton) exportButton.hidden = false;
    } catch (err) { show("batchResult", err.message); }
  });
  $("checkStatus").addEventListener("click", async () => {
    const paths = ["/api/health/", "/api/ingestion/status/"];
    const results = {};
    for (const path of paths) {
      try { results[path] = {available:true, response:await request(path)}; }
      catch (err) { results[path] = {available:false, detail:err.message}; }
    }
    show("statusResult", results);
  });

  async function runDatabaseDL(playerId, target, resultId, statusId) {
    const player = ($(playerId).value || "").trim();
    if (!player) { show(resultId, "Enter a player name."); return; }
    showLoading(resultId, "Loading the latest five historical matches and running the saved DL model…");
    try {
      const data = await request("/api/predict/dl/database/", {
        method: "POST",
        body: JSON.stringify({player_name: player, target: target})
      });
      show(resultId, data);
      const status = $(statusId);
      if (status) status.textContent = "Prediction completed for " + player + " using the database-driven five-match sequence.";
    } catch (err) {
      show(resultId, err.message);
      const status = $(statusId);
      if (status) status.textContent = "DL prediction failed. Check the error below and the registered model artifacts.";
    }
  }
  $("runBattingDL").addEventListener("click", () =>
    runDatabaseDL("battingDLPlayer", "next_match_runs", "battingDLResult", "battingDLStatus"));
  $("runBowlingDL").addEventListener("click", () =>
    runDatabaseDL("bowlingDLPlayer", $("bowlingDLTarget").value, "bowlingDLResult", "bowlingDLStatus"));

})();