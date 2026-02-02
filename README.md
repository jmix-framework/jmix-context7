# Jmix Documentation for Context7

This repository contains Jmix documentation and UI Samples prepared for uploading to [Context7](https://context7.com).

There are two main components: Python-based web scrapers that extract documentation from official Jmix sources, and the scraped content organized into structured documentation (HTML) and UI code samples (markdown). The scrapers target the official [Jmix documentation site](https://docs.jmix.io) and the [UI Samples](https://demo.jmix.io/ui-samples/) demo application.

Running scrapers:

```bash
cd tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python jmix_docs_scraper.py ../content/docs
python jmix_ui_samples_scraper.py ../content/ui-samples
```