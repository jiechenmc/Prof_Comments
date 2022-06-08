import os
from dotenv import load_dotenv

load_dotenv()


async def page_html(page, tag="*"):
    pg = await page.inner_html(tag)
    return pg


async def login(page):
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
    print("Waiting 10 seconds for DUO Authentication on device ...")


async def scrape_routes(soup, i):
    header = True
    for row in soup.find_all("tr"):
        with open("routes.tsv", "a+") as f:
            if header:
                row_content = row.text.split("\n\n")[1:]
                row_content = list(map(str.strip, row_content))
                sec = row_content[0]
                title = row_content[1]
                instructor = row_content[2]
                f.write(f"{i}\t{sec}\t{title}\t{instructor}\tRoute\n")
                header = False
            else:
                row_content = row.text.split("\n\n")[1:-1]
                row_content = list(map(str.strip, row_content))
                route = row.find("a").get("href")

                sec = row_content[0]
                title = row_content[1]

                try:
                    instructor = row_content[2]
                except IndexError:
                    instructor = ""

                res = f"{i}\t{sec}\t{title}\t{instructor}\t{route}\n"
                f.write(res)