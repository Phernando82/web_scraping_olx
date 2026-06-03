# OLX Price Scraper

Automated market data collector · Python · Selenium · CSV · WebDriver Manager

---

## Overview

Selenium-based scraper that autonomously traverses all paginated results for a given product search on OLX, extracting listing title, price, and URL from each page and appending records to a structured CSV file. Handles cookie consent dialogs, scroll-triggered lazy loading, and automatic pagination until the last page is reached. Demonstrates a complete autonomous data collection loop applicable to industrial supplier price monitoring, spare parts market intelligence, and asset valuation pipelines.

---

## Technical Highlights

**Automated WebDriver provisioning**
`webdriver_manager` resolves, downloads, and configures the correct ChromeDriver version at runtime — eliminating manual driver maintenance. Equivalent to automatic firmware/driver resolution in industrial device management platforms where field hardware versions vary across sites.

**Scroll-triggered content loading**
The crawler executes JavaScript scroll-to-bottom before extraction to force lazy-loaded listings into the DOM, then scrolls back to top before parsing. This two-pass scroll pattern reliably materializes dynamically injected content — the same challenge faced when scraping industrial dashboards or web-based HMI panels that render data progressively.

**Full pagination traversal**
After extracting each page, the crawler locates the forward pagination button via `data-testid` attribute and advances automatically, looping until the element is absent (last page reached). The exception-as-termination pattern provides clean exit without brittle page-count assumptions — equivalent to sequential register block reads in Modbus that advance until no response is returned.

**Browser hardening via Chrome options**
The driver is initialized with a controlled profile: fixed viewport, incognito mode, notifications suppressed, and auto-download enabled. Reduces session variability across runs — equivalent to deterministic environment configuration in industrial test automation where reproducibility is required.

**Incremental CSV append**
Each page's records are appended to `precos.csv` immediately after extraction rather than buffering in memory, ensuring partial results are preserved if the crawl is interrupted. Mirrors the write-through pattern used in industrial data loggers that flush records to storage on each acquisition cycle to prevent data loss on power failure.

---

## Stack

Python 3.x · Selenium · webdriver-manager · csv · time · os

---

## Installation

```bash
git clone https://github.com/Phernando82/web_scraping_olx.git
cd olx-price-scraper
pip install -r requirements.txt
```

Google Chrome must be installed. ChromeDriver is managed automatically.

```bash
python main.py
```

Output is written to `precos.csv` in the project root.

---

## Pipeline

```
iniciar_driver()
   │
   ▼
Navigate to OLX search URL
   │
   ▼
Accept cookie consent dialog
   │
   ▼
┌─ Page loop ──────────────────────────────────┐
│                                              │
│  scroll to bottom (trigger lazy load)        │
│  scroll to top                               │
│  extract: títulos · preços · links           │
│  append records → precos.csv                 │
│                                              │
│  pagination-forward button present?          │
│  ├── yes → click → next page                 │
│  └── no  → last page reached → break         │
└──────────────────────────────────────────────┘
   │
   ▼
driver.close()
```

---

## Output Format

`precos.csv` — semicolon-delimited, UTF-8:

```
Título do anúncio;Preço;https://www.olx.pt/d/anuncio/...
Super Nintendo completo;45 €;https://www.olx.pt/d/anuncio/...
```

---

## Relevance to Industry 4.0

The autonomous traversal → extract → persist pipeline maps directly to industrial data acquisition and market intelligence workflows:

- **Automated pagination traversal** → sequential polling of paginated API endpoints or register blocks (Modbus, DNP3) until end-of-data is signalled — same loop-until-no-response termination pattern
- **Scroll-triggered DOM materialization** → handling of web-based industrial dashboards (Ignition Perspective, Grafana) that progressively render data and require scroll or viewport interaction before full content is available
- **Incremental write-through to CSV** → industrial data logger pattern: flush each acquisition cycle to persistent storage immediately, preserving all records up to the point of any interruption
- **Spare parts price monitoring** → direct application in maintenance procurement: automated collection of market prices for critical spare parts (VFDs, PLCs, sensors) from secondary markets to support make-or-buy decisions and budget forecasting
- **Controlled browser profile** → deterministic environment configuration in industrial test automation and RPA (Robotic Process Automation) workflows where session reproducibility across runs is required

---

## Known Limitations

- XPath selectors are tied to OLX's current CSS class names — layout changes on the target site may require selector updates.
- No deduplication across runs; records are appended on each execution.

---

## License

MIT · Targets only publicly accessible listing pages. No authentication or private data is accessed.
