# Deal-Dex

**Deal-Dex** is a bot that watches for **Pokémon** and **Magic: The Gathering** card deals on **eBay** and **TCGplayer**.
It scans listings, checks them against your rules, and pushes alerts to **Discord (via Apprise)**.

![CI](https://img.shields.io/github/actions/workflow/status/your-org/deal-dex/ci.yml)
![License](https://img.shields.io/badge/license-MIT-informational)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue)

---

## ✨ Features

- Watches **eBay** & **TCGplayer** (singles & sealed)
- Filter by set, card name, price ceiling, rarity, condition, seller rating
- Detects under-market deals (% below comps)
- Avoids spam (dedupes, cooldowns)
- **Alerts directly to Discord** (via Apprise)
- Easy deployment with Docker, cron, or GitHub Actions

---

## 🧠 How it works

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌─────────────┐
│ Schedulers  │──▶──│ Market Feeds │──▶──│ Deal Engine│──▶──│ Apprise/Discord │
└─────────────┘     └──────────────┘     └────────────┘     └─────────────┘
```

1. Feeds pull listings from eBay & TCGplayer
2. Engine checks them against your rules (`rules.yml`)
3. Matching deals get pushed into **Discord**

---

## 📦 Tech stack

- Python 3.11+
- httpx / aiohttp
- Pydantic (config)
- SQLite (default storage)
- Typer (CLI)
- [Apprise](https://github.com/caronc/apprise) for notifications
- Docker (optional)

---

## 🚀 Quick start

### 1) Clone & install

```bash
git clone https://github.com/your-org/deal-dex.git
cd deal-dex
python scripts/setup_env.py
source .venv/bin/activate
```

### 2) Configure environment

Create `.env`:

```dotenv
# Database
DEALDEX_DB=sqlite+aiosqlite:///./data/deals.db

# eBay API
EBAY_APP_ID=your-ebay-app-id

# TCGplayer API
TCGPLAYER_PUBLIC_KEY=pk_xxx
TCGPLAYER_PRIVATE_KEY=sk_xxx

# Apprise targets (Discord webhook)
APPRISE_URLS=discord://webhook_id/webhook_token
```

> You can add multiple Apprise URLs, separated by commas.

### 3) Define your rules

`rules.yml`:

```yaml
defaults:
  currency: USD
  max_shipping: 6.00
  min_seller_feedback: 98
  exclude_keywords: ["proxy", "damaged", "heavy played"]

watches:
  - name: "MTG Staples"
    market: ["ebay", "tcgplayer"]
    include_keywords: ["Liliana of the Veil", "Fury"]
    condition: ["NM", "LP"]
    max_price: 35.00
    percent_below_market: 15

  - name: "Pokemon ETBs"
    market: ["ebay"]
    include_keywords: ["Elite Trainer Box"]
    set_filter: ["151", "Obsidian Flames"]
    condition: ["Sealed"]
    max_price: 45.00
```

### 4) Run the scanner

```bash
python -m dealdex scan --rules rules.yml
```

### 5) Run the API server

```bash
uvicorn dealdex.api:app --reload
```

Query card info:

```bash
curl http://localhost:8000/cards/Black%20Lotus
```

---

## 🔔 Alerts (Discord)

Alerts show:
- Card name + set
- Price + shipping
- % below reference
- Seller feedback
- Direct link to listing

---

## 🐳 Docker

```bash
docker build -t deal-dex .
docker run --rm -it   --env-file .env   -v $(pwd)/data:/app/data   deal-dex python -m dealdex scan --rules rules.yml
```

---

## ⏱ Scheduling

### Cron (Linux):

```bash
*/10 * * * * /usr/bin/docker run --rm   --env-file /home/ubuntu/deal-dex/.env   -v /home/ubuntu/deal-dex/data:/app/data   deal-dex python -m dealdex scan --rules /app/rules.yml
```

### GitHub Actions:

```yaml
name: schedule
on:
  schedule:
    - cron: "*/10 * * * *"
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: python -m dealdex scan --rules rules.yml
        env:
          EBAY_APP_ID: ${{ secrets.EBAY_APP_ID }}
          TCGPLAYER_PUBLIC_KEY: ${{ secrets.TCGPLAYER_PUBLIC_KEY }}
          TCGPLAYER_PRIVATE_KEY: ${{ secrets.TCGPLAYER_PRIVATE_KEY }}
          APPRISE_URLS: ${{ secrets.APPRISE_URLS }}
```

---

## 📜 License

MIT © You & Contributors
