# Day 28 — ML and DL Prediction Separation

- ML player-name endpoint: `/api/predict/player/` (existing workflow)
- Dedicated DL endpoint registered: `False`
- DL route detected: `none`
- The UI does not claim DL inference is available unless a dedicated route exists.
- Confirm sequence length, feature order, target mapping, model path, and matching preprocessing artifacts before enabling DL inference.
- Django check exit code: `0`
