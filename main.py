import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()


async def print_page(page):
    pg = await page.inner_html("*")
    print(pg)


async def main():
    async with async_playwright() as p:
        # Loading the page
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://classie-evals.stonybrook.edu/")

        ## Filling in NetID
        await page.fill("text=Username", os.getenv("netid"))
        await page.fill("text=Password >> nth=1", os.getenv("netid_password"))
        await page.locator(".login-button").click()

        ## On push page
        await page.reload()

        # Clicking the send push notification to log in
        frame = await page.query_selector("#duo_iframe")
        content = await frame.content_frame()
        await content.click("button >> nth=0")

        # Wait for me to authenticate
        print("sleeping for 5 seconds ...")
        await asyncio.sleep(5)

        ##
        await print_page(page)

        # Exiting ...
        await browser.close()


asyncio.run(main())