from requests import get
from bs4 import BeautifulSoup as bs
from re import search
from datetime import datetime
from babel.dates import format_datetime
from json import dump

pynews = {}

with open("bibliotecas.list") as f:
    libs = f.read().split("\n")

for lib in libs:
    hist_page = get(f"https://pypi.org/project/{lib.lower()}/#history")
    html = bs(hist_page.text, "html.parser")
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
        continue

    if p_date and p_ver:
        str_release = p_date.text.strip()
        str_version = p_ver.text.strip()
    else:
        continue

    last_release = datetime.strptime(str_release, "%b %d, %Y")
    if last_release.month == datetime.now().month:
        ver_page = get(f"https://pypi.org/project/{lib}/{str_version}")
        html = bs(ver_page.text, "html.parser")
        project_page = html.find("a", {"class": "vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed"})["href"]
        
        pynews[title] = {
            "release": format_datetime(
                last_release, 
                format="dd.MMMM.yyyy", 
                locale="pt_BR"
                ).title().replace(".", " de "),
            "version": str_version,
            "project_page": project_page
            }
        
with open("pynews.json", "w") as f:
    dump(pynews, f)

print("Pynews executado com sucesso!")
        