(() => {
 let timer;
 async function suggest(input) {
  const list = document.getElementById("ipl-player-suggestions");
  if (!list) return;
  const q = input.value.trim();
  if (!q) { list.replaceChildren(); return; }
  try {
   const r = await fetch("/api/players/suggestions/?q=" + encodeURIComponent(q), {headers: {"Accept":"application/json"}});
   if (!r.ok) return;
   const data = await r.json();
   list.replaceChildren(...(data.results || []).map(row => {
    const option = document.createElement("option"); option.value = row.player_name; return option;
   }));
  } catch (_) {}
 }
 document.addEventListener("input", e => {
  if (!e.target.matches("[data-player-autocomplete]")) return;
  clearTimeout(timer); timer = setTimeout(() => suggest(e.target), 180);
 });
})();
