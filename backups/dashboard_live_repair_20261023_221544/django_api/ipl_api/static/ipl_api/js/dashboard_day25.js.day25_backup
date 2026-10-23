(() => {
  const $ = (id) => document.getElementById(id);
  const status = $("statusMessage");
  const summaryUrl = "/api/eda/summary/";
  const playerUrl = "/api/players/";

  async function getJson(url) {
    const response = await fetch(url, { headers: { "Accept": "application/json" } });
    const text = await response.text();
    let data;
    try { data = text ? JSON.parse(text) : {}; }
    catch (_) { throw new Error(`Expected JSON from ${url}; got a non-JSON response (HTTP ${response.status}).`); }
    if (!response.ok) {
      const detail = data.detail || data.error || data.message || `HTTP ${response.status}`;
      throw new Error(String(detail));
    }
    return data;
  }

  async function loadSummary() {
    status.className = "alert alert-info";
    status.textContent = "Loading summary…";
    try {
      const data = await getJson(summaryUrl);
      const aliases = {
        playersMetric: ["players", "player_count", "total_players"],
        matchesMetric: ["matches", "match_count", "total_matches"],
        battingMetric: ["batting_records", "batting_count"],
        bowlingMetric: ["bowling_records", "bowling_count"]
      };
      const missing = [];
      for (const [id, keys] of Object.entries(aliases)) {
        const key = keys.find(k => Object.prototype.hasOwnProperty.call(data, k));
        if (key) $(id).textContent = Number(data[key]).toLocaleString();
        else { $(id).textContent = "—"; missing.push(keys[0]); }
      }
      if (missing.length) {
        status.className = "alert alert-warning";
        status.textContent = `Summary API responded, but these fields were absent: ${missing.join(", ")}.`;
      } else {
        status.className = "alert alert-success";
        status.textContent = "Summary loaded successfully.";
      }
    } catch (err) {
      status.className = "alert alert-danger";
      status.textContent = `Could not load summary: ${err.message}`;
    }
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[ch]);
  }

  function extractPlayers(data) {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.results)) return data.results;
    if (data && Array.isArray(data.players)) return data.players;
    if (data && Array.isArray(data.data)) return data.data;
    return null;
  }

  $("playerSearchForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = $("playerSearchInput").value.trim();
    const body = $("playerResults");
    const resultStatus = $("playerSearchStatus");
    if (!query) {
      resultStatus.textContent = "Enter a player name to search.";
      $("playerSearchInput").focus();
      return;
    }
    resultStatus.textContent = "Searching…";
    body.innerHTML = '<tr><td colspan="2">Loading…</td></tr>';
    $("playerSearchButton").disabled = true;
    try {
      const data = await getJson(`${playerUrl}?search=${encodeURIComponent(query)}&page=1&page_size=20`);
      const players = extractPlayers(data);
      if (players === null) {
        body.innerHTML = '<tr><td colspan="2">The API responded, but its JSON shape is not recognized. Inspect /api/players/ response.</td></tr>';
        resultStatus.textContent = "Search response format needs mapping.";
        return;
      }
      if (!players.length) {
        body.innerHTML = '<tr><td colspan="2">No matching players found.</td></tr>';
        resultStatus.textContent = "Search completed: no matches.";
        return;
      }
      body.innerHTML = players.map((p) => {
        const name = p.player_name ?? p.name ?? p.player ?? p.full_name ?? "Unnamed player";
        const details = Object.entries(p)
          .filter(([k, v]) => !["player_name", "name", "player", "full_name"].includes(k) && ["string", "number", "boolean"].includes(typeof v))
          .slice(0, 5)
          .map(([k, v]) => `${k}: ${v}`)
          .join(" • ");
        return `<tr><td>${escapeHtml(name)}</td><td>${escapeHtml(details || "Player record returned")}</td></tr>`;
      }).join("");
      resultStatus.textContent = `Found ${players.length} result(s).`;
    } catch (err) {
      body.innerHTML = '<tr><td colspan="2">Search failed. See the message above.</td></tr>';
      resultStatus.textContent = `Player search failed: ${err.message}. Confirm the endpoint supports the search parameter.`;
    } finally {
      $("playerSearchButton").disabled = false;
    }
  });

  $("refreshButton").addEventListener("click", loadSummary);
  // Automatically populate cards when the dashboard opens.
  loadSummary();
})(); 
