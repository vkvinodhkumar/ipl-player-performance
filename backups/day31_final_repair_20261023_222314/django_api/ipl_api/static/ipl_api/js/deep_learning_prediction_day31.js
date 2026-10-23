(() => {
 document.addEventListener("click", async event => {
  const button = event.target.closest("button");
  if (!button || !/run dl prediction/i.test(button.textContent || "")) return;
  let node = button;
  for (let i = 0; i < 6 && node && !(node.querySelector && node.querySelector("textarea")); i++) node = node.parentElement;
  const area = node && node.querySelector("textarea");
  const output = node && node.querySelector("pre, code, .prediction-output, .result");
  if (!area) return;
  let payload;
  try { payload = JSON.parse(area.value); } catch (_) { if (output) output.textContent = "Enter valid JSON."; return; }
  button.disabled = true;
  try {
   const response = await fetch("/api/predict/dl/", {method:"POST", headers:{"Content-Type":"application/json","Accept":"application/json"}, body:JSON.stringify(payload)});
   const text = await response.text();
   if (output) { try { output.textContent = JSON.stringify(JSON.parse(text), null, 2); } catch (_) { output.textContent = text; } }
  } catch (error) { if (output) output.textContent = String(error); }
  finally { button.disabled = false; }
 });
})();
