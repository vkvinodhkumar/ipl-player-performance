
(() => {
  function outputFor(button) {
    const card = button.closest(".card, .prediction-panel, section, form") || button.parentElement;
    return card ? (card.querySelector("pre, code, .prediction-output, .result, .output, [data-result]") || card.lastElementChild) : null;
  }
  document.addEventListener("click", async event => {
    const button = event.target.closest("[data-day31-dl-submit]");
    if (!button) return;
    const card = button.closest(".card, .prediction-panel, section, form") || button.parentElement;
    const area = card && card.querySelector("textarea");
    const output = outputFor(button);
    if (!area) { if (output) output.textContent = "DL input textarea not found in this panel."; return; }
    let payload;
    try { payload = JSON.parse(area.value); }
    catch (_) { if (output) output.textContent = "Enter valid JSON with target and a 5-row sequence."; return; }
    if (!payload.target || !Array.isArray(payload.sequence) || payload.sequence.length !== 5) {
      if (output) output.textContent = 'Expected {"target":"next_match_runs","sequence":[[...],[...],[...],[...],[...]]}.';
      return;
    }
    button.disabled = true;
    if (output) output.textContent = "Running saved DL model…";
    try {
      const response = await fetch("/api/predict/dl/", {
        method: "POST",
        credentials: "same-origin",
        headers: {"Content-Type": "application/json", "Accept": "application/json"},
        body: JSON.stringify(payload)
      });
      const raw = await response.text();
      let body;
      try { body = JSON.parse(raw); } catch (_) { body = {detail: raw.slice(0, 2000)}; }
      if (output) output.textContent = JSON.stringify(body, null, 2);
    } catch (error) {
      if (output) output.textContent = "Request failed: " + String(error);
    } finally {
      button.disabled = false;
    }
  });
})();
