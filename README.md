# Debasish Mukherjee Personal Website

Single-page professional website with a dedicated email options page. Contact is available only via email or LinkedIn.
Includes an AI-powered Digital Twin chat widget backed by OpenRouter via a local server proxy.

## Files
- `index.html` main profile page
- `email.html` email options page (default mail app, Gmail, Outlook, copy)
- `styles.css` styling
- `script.js` page reveal interactions
- `email.js` email page behavior
- `twin.js` Digital Twin widget logic
- `server.py` local server proxy for OpenRouter
- `FINE_SPEC.md` requirements
- `SECURITY_REPORT.md` security notes
- `tests/test_site.py` content and contact method tests
- `tests/test_digital_twin.py` Digital Twin widget tests

## Run Locally
For full Digital Twin functionality, run the server:
```
python server.py
```
Then open `http://localhost:8000` in a browser.

Static preview without chat:
- Open `index.html` in a browser
- Or use VS Code Live Server on `index.html`

## Tests
Run:
```
python tests/test_site.py
python tests/test_digital_twin.py
```

## Contact Policy
Only email and LinkedIn are provided. Phone numbers are intentionally excluded.
