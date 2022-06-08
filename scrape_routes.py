import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from scripts import page_html, login, scrape_routes


async def main():
    async with async_playwright() as p:
        # Loading the page
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://classie-evals.stonybrook.edu/")

        # Logging in to the page
        await login(page)
        await asyncio.sleep(10)

        # Ready to scrape routes
        # Currently there are 1336 pages
        for i in range(1, 1337):
            url = "https://classie-evals.stonybrook.edu/?currentTerm=ALL&page="
            await page.goto(f"{url}{i}", timeout=0)
            soup = BeautifulSoup(await page_html(page, "table"), "html.parser")
            await scrape_routes(soup, i)

        # Exiting ...
        await browser.close()


asyncio.run(main())