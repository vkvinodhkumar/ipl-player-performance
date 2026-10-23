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

  // Live player autocomplete with fallback API contracts.
  const playerInputs = ["playerName", "battingPlayer", "bowlingPlayer", "battingDLPlayer", "bowlingDLPlayer"].map(id => $(id)).filter(Boolean);
  let playerSearchTimer = null;
  async function refreshPlayerOptions(query) {
    const list = $("playerOptions");
    if (!list || query.trim().length < 2) return;
    const urls = [
      "/api/players/search-options/?q=" + encodeURIComponent(query),
      "/api/players/?search=" + encodeURIComponent(query),
      "/api/players/search/?q=" + encodeURIComponent(query)
    ];
    for (const url of urls) {
      try {
        const data = await request(url);
        const rows = Array.isArray(data) ? data : (data.results || data.players || data.data || []);
        const names = rows.map(row => typeof row === "string" ? row : (row.player_name || row.name || row.full_name || row.player || "")).filter(Boolean);
        if (!names.length) continue;
        const existing = new Set(Array.from(list.options).map(o => o.value.toLowerCase()));
        names.forEach(name => {
          if (!existing.has(name.toLowerCase())) {
            const option = document.createElement("option"); option.value = name; list.appendChild(option); existing.add(name.toLowerCase());
          }
        });
        return;
      } catch (_) { /* Try next endpoint. */ }
    }
  }
  playerInputs.forEach(input => input.addEventListener("input", () => {
    clearTimeout(playerSearchTimer);
    playerSearchTimer = setTimeout(() => refreshPlayerOptions(input.value), 250);
  }));

  async function withLoading(buttonId, resultId, action) {
    const button = $(buttonId), original = button ? button.textContent : "";
    if (button) { button.disabled = true; button.textContent = "Predicting…"; }
    show(resultId, "⏳ Prediction in progress. Please wait…");
    try { await action(); } finally { if (button) { button.disabled = false; button.textContent = original; } }
  }
  async function prediction(endpoint, playerId, jsonId, resultId, buttonId, fixedTarget) {
    try {
      await withLoading(buttonId, resultId, async () => {
        const player = ($(playerId).value || "").trim(), raw = ($(jsonId).value || "").trim();
        let payload;
        if (raw) payload = safeParse(raw, "Feature payload");
        else if (player) {
          const target = fixedTarget || ($("bowlingMLTarget") ? $("bowlingMLTarget").value : "next_match_wickets");
          const data = await request("/api/predict/player/", {method:"POST", body:JSON.stringify({player_name:player, target:target})});
          show(resultId, {player_name:player, target:target, prediction:data}); return;
        } else throw new Error("Enter a player name or provide feature JSON.");
        show(resultId, await request(endpoint, {method:"POST", body:JSON.stringify(payload)}));
      });
    } catch (err) { show(resultId, "Prediction failed: " + err.message); }
  }
  $("runBattingML").addEventListener("click", () => prediction("/api/predict/batting/", "battingPlayer", "battingJson", "battingMLResult", "runBattingML", "next_match_runs"));
  $("runBowlingML").addEventListener("click", () => prediction("/api/predict/bowling/", "bowlingPlayer", "bowlingJson", "bowlingMLResult", "runBowlingML"));

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

  async function runDatabaseDL(playerId, jsonId, target, resultId, statusId, buttonId) {
    const player = (($(playerId) && $(playerId).value) || "").trim();
    const raw = (($(jsonId) && $(jsonId).value) || "").trim();
    const status = $(statusId);
    try {
      await withLoading(buttonId, resultId, async () => {
        let payload;
        if (raw) { payload = safeParse(raw, "DL input JSON"); payload.target = payload.target || target; if (player) payload.player_name = player; }
        else if (player) payload = {player_name:player, target:target};
        else throw new Error("Enter a player name or provide DL input JSON.");
        if (status) status.textContent = "Prediction running…";
        const data = await request("/api/predict/dl/database/", {method:"POST", body:JSON.stringify(payload)});
        show(resultId, {player_name:player || payload.player_name || null, target:payload.target, prediction:data});
        if (status) status.textContent = "Prediction completed.";
      });
    } catch (err) {
      show(resultId, "Prediction failed: " + err.message);
      if (status) status.textContent = "Prediction failed. See the error below.";
    }
  }
  $("runBattingDL").addEventListener("click", () => runDatabaseDL("battingDLPlayer", "battingDLJson", "next_match_runs", "battingDLResult", "battingDLStatus", "runBattingDL"));
  $("runBowlingDL").addEventListener("click", () => runDatabaseDL("bowlingDLPlayer", "bowlingDLJson", $("bowlingDLTarget").value, "bowlingDLResult", "bowlingDLStatus", "runBowlingDL"));

})();