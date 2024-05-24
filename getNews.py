from json import dump
from datetime import datetime
import asyncio
from bs4 import BeautifulSoup as bs
from babel.dates import format_datetime
import aiohttp

from cacheVariables import pynews


async def fetch(session, url):
    async with session.get(f"https://pypi.org/project/{url.lower()}/#history") as response:
        body = await response.text()
        html = bs(body, "html.parser")
        title = html.title.decode()
        title = title[title.find(">") + 1: title.find(" ")].title()
        div_release = html.find(
            "div",
            {"class": "release release--latest release--current"}
        )
        if div_release:
            p_date = div_release.find(
                "p",
                {"class": "release__version-date"}
            )

            p_ver = div_release.find(
                "p",
                {"class": "release__version"}
            )
        else:
            return

        if p_date and p_ver:
            str_release = p_date.text.strip()
            str_version = p_ver.text.strip()
        else:
            return

        last_release = datetime.strptime(str_release, "%b %d, %Y")
        if last_release.month == datetime.now().month:
            async with session.get(f"https://pypi.org/project/{url.lower()}/{str_version}") as ver_page:
                body = await ver_page.text()
                html = bs(body, "html.parser")
                project_page = html.find(
                    "a", {"class": "vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed"})["href"]
                pynews[title] = {
                    "release": format_datetime(
                        last_release,
                        format="dd.MMMM.yyyy",
                        locale="pt_BR"
                    ).title().replace(".", " de "),
                    "version": str_version,
                    "project_page": project_page
                }


with open("bibliotecas.list") as f:
    libs = f.read().split("\n")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for url in libs]
        await asyncio.gather(*tasks)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())

with open("pynews.json", "w") as f:
    dump(pynews, f)

print("Pynews executado com sucesso!")
