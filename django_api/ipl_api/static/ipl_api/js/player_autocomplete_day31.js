
(() => {
  const endpoint = "/api/players/suggestions/";
  let timer = null;
  function ensureDatalist() {
    let list = document.getElementById("ipl-player-suggestions");
    if (!list) {
      list = document.createElement("datalist");
      list.id = "ipl-player-suggestions";
      document.body.appendChild(list);
    }
    return list;
  }
  function isPlayerInput(el) {
    if (!(el instanceof HTMLInputElement)) return false;
    const text = [
      el.name, el.id, el.placeholder, el.getAttribute("aria-label"),
      el.closest(".card, section, form")?.innerText?.slice(0, 500)
    ].filter(Boolean).join(" ").toLowerCase();
    return /player.?name|player name|player search|historical performance|batting predictions|bowling predictions/.test(text);
  }
  async function loadSuggestions(input) {
    const query = input.value.trim();
    const list = ensureDatalist();
    if (query.length < 1) { list.replaceChildren(); return; }
    try {
      const response = await fetch(endpoint + "?q=" + encodeURIComponent(query), {
        method: "GET", headers: {"Accept": "application/json"}, credentials: "same-origin"
      });
      if (!response.ok) return;
      const body = await response.json();
      list.replaceChildren(...(body.results || []).map(row => {
        const option = document.createElement("option");
        option.value = row.player_name;
        return option;
      }));
      input.setAttribute("list", list.id);
      input.setAttribute("autocomplete", "off");
    } catch (error) {
      console.warn("Player suggestions unavailable:", error);
    }
  }
  document.addEventListener("focusin", event => {
    if (isPlayerInput(event.target)) {
      event.target.setAttribute("list", "ipl-player-suggestions");
      ensureDatalist();
    }
  });
  document.addEventListener("input", event => {
    if (!isPlayerInput(event.target)) return;
    event.target.setAttribute("list", "ipl-player-suggestions");
    clearTimeout(timer);
    timer = setTimeout(() => loadSuggestions(event.target), 160);
  });
})();
