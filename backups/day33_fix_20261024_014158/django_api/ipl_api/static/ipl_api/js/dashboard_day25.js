(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const jsonText = value => JSON.stringify(value, null, 2);
  const show = (id, value) => { const el = $(id); if (el) el.textContent = typeof value === "string" ? value : jsonText(value); };
  const safeParse = (raw, label) => {
    try { return JSON.parse(raw); }
    catch (err) { throw new Error(label + " is not valid JSON: " + err.message); }
  };
  function getCookie(name) {
    const prefix = name + "=";
    for (const part of (document.cookie || "").split(";")) {
      const item = part.trim();
      if (item.startsWith(prefix)) return decodeURIComponent(item.slice(prefix.length));
    }
    return "";
  }
  async function request(url, options = {}) {
    const method = (options.method || "GET").toUpperCase();
    const headers = {
      "Accept": "application/json",
      ...(options.body ? {"Content-Type": "application/json"} : {}),
      ...(options.headers || {})
    };
    if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method)) {
      const token = getCookie("csrftoken");
      if (token) headers["X-CSRFToken"] = token;
    }
    const response = await fetch(url, {...options, method, credentials: "same-origin", headers});
    const raw = await response.text();
    let body;
    try { body = raw ? JSON.parse(raw) : null; } catch { body = raw; }
    if (!response.ok) {
      const detail = body && typeof body === "object" ? (body.detail || body.error || body.message || body) : body;
      throw new Error("HTTP " + response.status + " from " + url + ": " + (typeof detail === "string" ? detail : JSON.stringify(detail)));
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

  // Live player autocomplete; the API must expose at least one supported search path.
  const playerInputs = ["playerName", "battingPlayer", "bowlingPlayer", "battingDLPlayer", "bowlingDLPlayer"].map(id => $(id)).filter(Boolean);
  let playerSearchTimer = null, latestPlayerQuery = "";
  async function refreshPlayerOptions(query) {
    const list = $("playerOptions");
    query = (query || "").trim();
    if (!list || query.length < 2) return;
    latestPlayerQuery = query;
    const urls = [
      "/api/players/?search=" + encodeURIComponent(query),
      "/api/players/search/?q=" + encodeURIComponent(query),
      "/api/players/search-options/?q=" + encodeURIComponent(query)
    ];
    for (const url of urls) {
      try {
        const data = await request(url);
        const rows = Array.isArray(data) ? data : (data.results || data.players || data.data || data.matches || []);
        const names = rows.map(row => typeof row === "string" ? row : (row.player_name || row.name || row.full_name || row.player || "")).filter(Boolean);
        if (query !== latestPlayerQuery) return;
        if (names.length) {
          list.replaceChildren();
          [...new Set(names)].forEach(name => { const option = document.createElement("option"); option.value = name; list.appendChild(option); });
          return;
        }
      } catch (_) {}
    }
  }
  playerInputs.forEach(input => input.addEventListener("input", () => {
    clearTimeout(playerSearchTimer);
    playerSearchTimer = setTimeout(() => refreshPlayerOptions(input.value), 250);
  }));

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
  /* DAY33_ROBUST_UI_PATCH */
  (function(){
    const byId=id=>document.getElementById(id);
    const playerIds=["playerName","battingPlayer","battingDLPlayer","bowlingPlayer","bowlingDLPlayer"];
    const inputs=playerIds.map(byId).filter(Boolean);
    const list=byId("playerOptions");
    let active=null, timer=null;
    const menu=document.createElement("div");
    menu.className="list-group shadow";
    menu.style.cssText="position:absolute;z-index:99999;display:none;max-height:240px;overflow-y:auto;background:white;";
    document.body.appendChild(menu);
    function close(){menu.style.display="none";menu.replaceChildren();active=null;}
    function namesFrom(d){
      const rows=Array.isArray(d)?d:(d&&(d.results||d.players||d.options||d.data))||[];
      if(!Array.isArray(rows))return [];
      return [...new Set(rows.map(v=>typeof v==="string"?v:(v.player_name||v.name||v.full_name||v.label||v.value)).filter(v=>typeof v==="string"&&v.trim()))];
    }
    async function getNames(q){
      const base="/api/players/search-options/";
      for(const url of [base+"?q="+encodeURIComponent(q),base+"?search="+encodeURIComponent(q),base]){
        try{
          const r=await fetch(url,{credentials:"same-origin",headers:{"Accept":"application/json"}});
          if(!r.ok)continue;
          const n=namesFrom(await r.json()); if(n.length)return n;
        }catch(e){}
      }
      return [];
    }
    inputs.forEach(input=>{
      input.setAttribute("autocomplete","off");
      input.addEventListener("input",()=>{
        clearTimeout(timer); const q=input.value.trim(); active=input;
        if(q.length<2){close();return;}
        timer=setTimeout(async()=>{
          const results=(await getNames(q)).filter(n=>n.toLowerCase().includes(q.toLowerCase())).slice(0,12);
          if(active!==input)return;
          if(list)list.replaceChildren(...results.map(n=>{const o=document.createElement("option");o.value=n;return o;}));
          menu.replaceChildren();
          if(!results.length){close();return;}
          const r=input.getBoundingClientRect();
          menu.style.left=(r.left+window.scrollX)+"px";menu.style.top=(r.bottom+window.scrollY)+"px";menu.style.width=r.width+"px";menu.style.display="block";
          results.forEach(n=>{const b=document.createElement("button");b.type="button";b.className="list-group-item list-group-item-action";b.textContent=n;
            b.addEventListener("mousedown",e=>{e.preventDefault();input.value=n;close();input.dispatchEvent(new Event("change",{bubbles:true}));});
            menu.appendChild(b);});
        },180);
      });
      input.addEventListener("blur",()=>setTimeout(close,180));
    });
    // Loading indicator on any prediction button, independent of the existing handler name.
    const predictionButtons=[...document.querySelectorAll("button")].filter(b=>/run .*prediction|predict/i.test(b.textContent||""));
    predictionButtons.forEach(button=>{
      button.addEventListener("click",()=>{
        if(button.disabled)return;
        if(button.dataset.day33Busy==="1")return;
        button.dataset.day33Busy="1";
        button.dataset.day33Original=button.innerHTML;
        button.disabled=true;
        button.innerHTML='<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Predicting…';
        // The request can take time. Restore after existing code finishes or after a safe timeout.
        const restore=()=>{if(button.dataset.day33Busy!=="1")return;button.disabled=false;button.innerHTML=button.dataset.day33Original||"Run prediction";button.dataset.day33Busy="0";};
        const observer=new MutationObserver(()=>{if(!button.isConnected){observer.disconnect();return;}});
        observer.observe(document.body,{childList:true,subtree:true});
        setTimeout(()=>{restore();observer.disconnect();},60000);
        // Existing request/result handlers generally update the result pane; restore once it changes.
        const result=button.closest(".card")?.querySelector("pre, .prediction-result, [id$='Result']");
        if(result){const mo=new MutationObserver(()=>{restore();mo.disconnect();});mo.observe(result,{childList:true,subtree:true,characterData:true});}
      },true);
    });
  })();


})();