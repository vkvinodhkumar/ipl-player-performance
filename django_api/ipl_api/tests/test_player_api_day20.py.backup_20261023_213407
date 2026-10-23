from django.test import SimpleTestCase
from unittest.mock import patch

class PlayerApiSmokeTests(SimpleTestCase):
    @patch("ipl_api.views.fetch_all")
    def test_player_list_returns_paginated_json(self, mock_fetch_all):
        mock_fetch_all.side_effect = [
            [{"total": 2}],
            [{"player_name": "Virat Kohli"}, {"player_name": "Rohit Sharma"}],
        ]
        response = self.client.get("/api/players/?page=1&page_size=2", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 2)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(len(payload["results"]), 2)

    @patch("ipl_api.views.fetch_all")
    def test_player_detail_returns_aggregates(self, mock_fetch_all):
        mock_fetch_all.side_effect = [
            [{"batting_records": 1, "matches": 1, "runs": 42, "balls_faced": 30, "fours": 4, "sixes": 1}],
            [{"bowling_records": 0, "matches": 0, "wickets": 0, "runs_conceded": 0, "overs": 0}],
        ]
        response = self.client.get("/api/players/Virat%20Kohli/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["player_name"], "Virat Kohli")
        self.assertEqual(payload["batting"]["runs"], 42)

    @patch("ipl_api.views.fetch_all")
    def test_unknown_player_returns_404(self, mock_fetch_all):
        mock_fetch_all.side_effect = [
            [{"batting_records": 0, "matches": 0, "runs": 0, "balls_faced": 0, "fours": 0, "sixes": 0}],
            [{"bowling_records": 0, "matches": 0, "wickets": 0, "runs_conceded": 0, "overs": 0}],
        ]
        response = self.client.get("/api/players/__day20_unknown_player__/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 404)
