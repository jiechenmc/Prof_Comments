import os
import re
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


async def scrape_routes_to_file(soup, i, file_name, header=True):
    for row in soup.find_all("tr"):
        with open("./" + "routes.tsv", "a+") as f:
            term = file_name.replace(".tsv", "").replace("_", " ")
            try:
                if header:
                    row_content = row.text.split("\n\n")[1:]
                    row_content = list(map(str.strip, row_content))
                    sec = row_content[0]
                    title = row_content[1]
                    instructor = row_content[2]
                    f.write(
                        f"{i}\t{sec}\tTerm\t{title}\t{instructor}\tRoute\n")
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

                    res = f"{i}\t{sec}\t{term}\t{title}\t{instructor}\t{route}\n"
                    f.write(res)
            except AttributeError:
                # AttributeError only on header rows
                pass


async def parse_script_tag(scripts):
    # Cleaning the data
    pattern = re.compile(r".+\[.+\]")
    for script in scripts:
        if "drawChartGradeDistAFPNC" in script.text:
            result = re.findall(pattern, str(script))
            result = result[1:16]

            grades = []
            for res in result:
                res = res.strip().split(",")[0:2]
                for i, r in enumerate(res):
                    res[i] = r.replace("[", "").strip("'").strip()
                grades.append(tuple(res))
    return grades


async def scrape_content(soup):
    try:
        section1 = soup.find("ul", {"id": "paginate-1"})
        comments1 = section1.find_all("li")

        section2 = soup.find("ul", {"id": "paginate-2"})
        comments2 = section2.find_all("li")

        scripts = soup.find_all("script", {"type": "text/javascript"})

        grades = await parse_script_tag(scripts)

        valuable = [comment.text.strip() for comment in comments1]
        improve = [comment.text.strip() for comment in comments2]

        valuable.extend(improve)

        return valuable, grades

    except AttributeError:
        # This happens when grade distribution is not available
        try:
            section3 = soup.find("ul", {"id": "paginate-3"})
            comments3 = section3.find_all("li")

            scripts = soup.find_all("script", {"type": "text/javascript"})

            grades = await parse_script_tag(scripts)

            additional = [comment.text.strip() for comment in comments3]

            return additional, []
        except Exception:
            # Any furthur Exception means no content.
            return [], []