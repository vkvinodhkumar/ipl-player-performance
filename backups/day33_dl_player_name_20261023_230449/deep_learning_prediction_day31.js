(() => {
  function panelFor(button) {
    return button.closest(".card") || button.closest(".col") || button.parentElement.parentElement;
  }
  function resultBox(panel) {
    return panel.querySelector("[data-day31-dl-result]") ||
      panel.querySelector("pre") || panel.querySelector("code") ||
      panel.querySelector(".result, .output, .prediction-output") ||
      panel.lastElementChild;
  }
  document.addEventListener("click", async event => {
    const button = event.target.closest("[data-day31-dl-submit]");
    if (!button) return;
    const panel = panelFor(button);
    const area = panel.querySelector("textarea");
    const out = resultBox(panel);
    const show = value => { if (out) out.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2); };
    if (!area) { show("DL input field not found in this panel."); return; }
    let payload;
    try { payload = JSON.parse(area.value); }
    catch (e) { show("Invalid JSON: include target and a 5-row sequence."); return; }
    if (!["next_match_runs", "next_match_wickets", "next_match_runs_conceded"].includes(payload.target) ||
        !Array.isArray(payload.sequence) || payload.sequence.length !== 5 ||
        !payload.sequence.every(row => Array.isArray(row) && row.length > 0 && row.every(v => typeof v === "number" && Number.isFinite(v)))) {
      show({detail: "Payload must include a supported target and five chronological numeric rows.", example:
        {target:"next_match_runs", sequence:[[0,0],[0,0],[0,0],[0,0],[0,0]]}});
      return;
    }
    button.disabled = true;
    show("Loading saved Day 12 model and preprocessing…");
    try {
      const response = await fetch("/api/predict/dl/", {
        method: "POST", credentials: "same-origin",
        headers: {"Content-Type":"application/json", "Accept":"application/json"},
        body: JSON.stringify(payload)
      });
      const raw = await response.text();
      let data; try { data = JSON.parse(raw); } catch (_) { data = {detail: raw.slice(0, 1800)}; }
      show({http_status: response.status, ...data});
    } catch (err) { show("Request failed: " + String(err)); }
    finally { button.disabled = false; }
  });
})();
