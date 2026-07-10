# Alter

An offline-first currency exchange web app. It loads instantly from cache, works with no internet connection, and refreshes its exchange rates automatically whenever it is online.

## How it works

- A **service worker** caches the entire app on first visit, so later visits load instantly and work fully offline.
- Exchange rates are fetched from the free [Exchange Rate API](https://www.exchangerate-api.com) (160+ currencies), saved to local storage, and reused offline.
- On every launch — and whenever the connection comes back — stale rates (older than 1 hour) are refreshed in the background.
- A bundled rate snapshot means conversions work even if the app has never been online.
- Installable as a PWA (Add to Home Screen) for one-tap access.

## Running locally

No build step. Serve the folder over HTTP (service workers require http/https):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Or deploy the folder as-is to any static host (GitHub Pages, Netlify, etc.).

## License

GPL v3 — see [LICENSE](LICENSE).
