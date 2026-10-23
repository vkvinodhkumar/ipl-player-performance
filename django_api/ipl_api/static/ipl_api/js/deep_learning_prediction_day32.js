(() => {
  document.addEventListener("click", async event => {
    const button = event.target.closest("[data-day31-dl-submit]");
    if (!button) return;
    const panel = button.closest(".card") || button.closest(".col") || button.parentElement?.parentElement || document;
    const area = panel.querySelector("textarea");
    const out = panel.querySelector("pre, .prediction-output, .result, .output") || panel.lastElementChild;
    const show = value => { if (out) out.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2); };
    if (!area) return show("DL sequence input not found.");
    let payload;
    try { payload = JSON.parse(area.value); } catch (_) { return show("Enter valid JSON."); }
    if (!["next_match_runs","next_match_wickets","next_match_runs_conceded"].includes(payload.target))
      return show({detail:"Use a supported target: next_match_runs, next_match_wickets, next_match_runs_conceded."});
    if (!Array.isArray(payload.sequence) || payload.sequence.length !== 5 ||
        !payload.sequence.every(r => Array.isArray(r) && r.length > 0 && r.every(v => typeof v === "number" && Number.isFinite(v))))
      return show({detail:"sequence must contain five chronological arrays of finite numeric feature values."});
    if (payload.preprocessed === true) return show({detail:"Remove preprocessed:true. Send raw Day 11 ordered features; server applies Day 12 imputer/scaler."});
    button.disabled = true; show("Running saved DL model…");
    try {
      const response = await fetch("/api/predict/dl/", {method:"POST", credentials:"same-origin",
        headers:{"Content-Type":"application/json","Accept":"application/json"}, body:JSON.stringify(payload)});
      const raw = await response.text(); let data;
      try { data = JSON.parse(raw); } catch (_) { data = {detail:raw.slice(0,2500)}; }
      data.http_status = response.status; show(data);
    } catch (e) { show({detail:"Request failed", error:String(e)}); }
    finally { button.disabled = false; }
  });
})();