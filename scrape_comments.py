import asyncio
from playwright.async_api import async_playwright
from modules.scrape.scripts import login, page_html, scrape_content
from bs4 import BeautifulSoup
from playwright._impl._api_types import TimeoutError, Error


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://classie-evals.stonybrook.edu/")

        # Logging in to the page
        await login(page)
        await asyncio.sleep(10)

        with open("data/routes.tsv", "r") as f:
            header = True
            # [start:]
            # start + 1 from routes.tsv is getting skipped
            f = f.readlines()[12393:]
            for line in f:
                if header == True:
                    header = False
                else:
                    try:
                        line = line.split("\t")
                        page_url = "https://classie-evals.stonybrook.edu" + line[
                            4]
                        await page.goto(page_url)

                        soup = BeautifulSoup(await page_html(page),
                                             "html.parser")

                        ## scrape content from page
                        res = await scrape_content(soup)
                        with open("data/comments.tsv", "a") as f:
                            string = f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\t{res}\n"
                            f.write(string)
                    except (TimeoutError, Error):
                        continue

        await browser.close()


asyncio.run(main())