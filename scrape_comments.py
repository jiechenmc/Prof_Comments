import asyncio
import sys
from datetime import datetime as dt
from datetime import timedelta
from playwright.async_api import async_playwright
from modules.scrape.scripts import login, page_html, scrape_content
from bs4 import BeautifulSoup
from playwright._impl._api_types import TimeoutError, Error


###
#
# Sample Execution
# python scrape_comments.py start
# python scrape_comments.py 1
# Scraping will start from line 1 of routes.tsv
# Note: if line 1 is the header row; start from line 2 instead.
###
async def main():
    start = int(sys.argv[1])
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://classie-evals.stonybrook.edu/")

        # Logging in to the page
        # Duo tokens expires every 30 minutes
        await login(page)
        await asyncio.sleep(10)

        now = dt.now()
        expire = now + timedelta(minutes=20)
        print(
            f"Session started at: {now:%I:%M}\nDuo Token Expires in 20 minutes: {expire:%I:%M}"
        )

        with open("data/routes.tsv", "r") as f:
            # [start:]
            # Begins at start + 1 from routes.tsv
            f = f.readlines()[start - 1:]

            for line in f:
                try:
                    line = line.split("\t")
                    page_url = "https://classie-evals.stonybrook.edu" + line[5]

                    await page.goto(page_url)

                    soup = BeautifulSoup(await page_html(page), "html.parser")

                    ## scrape content from page
                    res = await scrape_content(soup)
                    with open("data/comments.tsv", "a") as f:
                        string = f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\t{line[4]}\t{res}\n"
                        f.write(string)
                except (TimeoutError, Error):
                    continue

        await browser.close()


asyncio.run(main())