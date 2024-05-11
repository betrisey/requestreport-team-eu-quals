import logging
import os
from time import sleep

from playwright.sync_api import sync_playwright

FLAG = os.getenv("FLAG")
FLAG_URL = os.getenv("FLAG_URL")

logging.basicConfig(level=logging.INFO)

def visit(url: str):
    if not url.startswith("http://") and not url.startswith("https://"):
        logging.info(f"Invalid URL: {url}")
        return

    logging.info(f"Visiting: {url}")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context()
        context.set_default_timeout(5000)
        context.add_cookies([{
            "name": "flag",
            "value": FLAG,
            "secure": True,
            "httpOnly": True,
            "sameSite": "Strict",
            "url": FLAG_URL
        }])

        page = context.new_page()
        page.goto(url)
        sleep(10)
        browser.close()
