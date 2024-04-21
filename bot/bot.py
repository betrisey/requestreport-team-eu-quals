import logging
import os
from time import sleep

from playwright.sync_api import sync_playwright

SECRET = os.getenv("SECRET")
COOKIE_URL = os.getenv("COOKIE_URL")

logging.basicConfig(level=logging.INFO)

def visit(url: str):
    if not url.startswith("http://") and not url.startswith("https://"):
        logging.info(f"Invalid URL: {url}")
        return

    logging.info(f"Visiting: {url}")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)

        context = browser.new_context(ignore_https_errors=True, user_agent="AAAAAA")
        context.set_default_timeout(5000)
        context.add_cookies([{
            "name": "secret",
            "value": SECRET,
            "secure": True,
            "httpOnly": True,
            "sameSite": "Lax",
            "url": COOKIE_URL
        }])

        page = context.new_page()
        page.goto(url)
        sleep(10)
        browser.close()
