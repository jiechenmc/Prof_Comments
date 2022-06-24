import asyncio
import sys
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from modules.scrape.scripts import page_html, login, scrape_routes_to_file


###
#
# Sample Execution
# python scrape_routes.py term url lastPageNumber
# python scrape_routes.py Spring_2022 https://classie-evals.stonybrook.edu/\?currentTerm\=1224\&page\= 73
#
###
async def main():
    # Term Url sys.argv[2]
    # https://classie-evals.stonybrook.edu/?currentTerm=1224&page=
    # Last Page sys.argv[3]

    term = sys.argv[1] + ".tsv"
    url = sys.argv[2]
    end = int(sys.argv[3]) + 1

    async with async_playwright() as p:
        # Loading the page
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://classie-evals.stonybrook.edu/")

        # Logging in to the page
        await login(page)
        await asyncio.sleep(10)

        # Ready to scrape routes
        for i in range(1, end):
            await page.goto(f"{url}{i}", timeout=0)
            soup = BeautifulSoup(await page_html(page, "table"), "html.parser")
            await scrape_routes_to_file(soup, i, term)

        # Exiting ...
        await browser.close()


asyncio.run(main())