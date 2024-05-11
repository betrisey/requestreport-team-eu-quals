import axios from "axios";
import React, { useState } from "react";
import SyntaxHighlighter from 'react-syntax-highlighter';
import { vs } from 'react-syntax-highlighter/dist/esm/styles/hljs';

function Report({ setSession }) {
  const formRef = React.useRef();
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    try {
      const response = await axios.post(
        "/app/visit",
        `url=${url}`,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );
      if (response.data.success) {
        setResult("A bot has been dispatched to visit the URL");
      } else {
        setResult(response.data.error || "An error occurred");
      }
    } catch (err) {
      setResult(err.response?.data?.error || "An error occurred");
    }
  };

  const botCode = `import logging
import os
from time import sleep

from playwright.sync_api import sync_playwright

FLAG = os.getenv("FLAG")

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
            "url": "${location.origin}/flag/"
        }])

        page = context.new_page()
        page.goto(url)
        sleep(10)
        browser.close()
`;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-4">report</h2>
      <div className="p-6 bg-white shadow-md rounded-lg">
        <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
          <input
            type="url"
            name="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required={true}
            className="input input-bordered w-full rounded-lg shadow-sm"
          />
          <button
            type="submit"
            className="btn btn-primary rounded-lg px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300"
          >
            Submit
          </button>
          {result && <p>{result}</p>}
        </form>
        <br />
        <SyntaxHighlighter language="python" style={vs}>
          {botCode}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}

export default Report;
