import asyncio
import json
import sys
import time
from datetime import datetime
from json import dump

from bibliotecas import bibliotecas
from cacheVariables import pynews
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
)
from prompt import Smart

md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(),
    options={
        "ignore_links": True,
        "escape_html": False,
        "ignore_images": True,
        "skip_internal_links": True,
    },
)
config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator,
)

news_json_file = "pynews.json"


class PyNews:
    def __init__(self):
        self.study_case = bibliotecas.copy()

    def check_for_release_url(self, lib):
        if lib.get("fixed_release_url", None):
            return lib["fixed_release_url"]
        else:
            return Smart().think_about_release_url(
                lib["releases_urls_list"], lib["version"]
            )

    async def fetch(self, lib, url_name):
        browser_config = BrowserConfig(
            browser_type="chromium",
            headless=True,
            text_mode=True,
            light_mode=True,
            extra_args=["--disable-extensions"],
        )
        async with AsyncWebCrawler(
            config=browser_config, verbose=True
        ) as crawler:
            html = await crawler.arun(
                url=lib[url_name],
                excluded_tags=["form", "header", "footer", "nav"],
                exclude_social_media_links=True,
                exclude_external_images=True,
                config=config,
            )
            new_html = html.markdown_v2

            response = {}
            count = 3
            try:
                response = Smart().answer(url_name, lib, new_html.fit_markdown)
            except Exception as e:
                print("Biblioteca não processada :", lib["library_name"])
                print(e)
            release_date = response.get("release_date")

            if response.get("release_date"):
                release_date = datetime.strptime(release_date, "%Y-%m-%d")
                if (datetime.now() - release_date).days <= 30:
                    lib["version"] = response["version"]
                    response["releases_doc_url"] = self.check_for_release_url(
                        lib
                    )
                    response["library_name"] = lib["library_name"]
                    pynews[lib["library_name"]] = response
            elif response.get("news"):
                pynews[lib["library_name"]] = response
                pynews[lib["library_name"]]["library_name"] = lib[
                    "library_name"
                ]
                pynews[lib["library_name"]]["logo"] = bibliotecas[
                    lib["library_name"]
                ]["logo"]
                pynews[lib["library_name"]]["version"] = lib["version"]
                pynews[lib["library_name"]]["release_date"] = lib[
                    "release_date"
                ]
                pynews[lib["library_name"]]["releases_doc_url"] = lib[
                    "releases_doc_url"
                ]
                if bibliotecas[lib["library_name"]].get("fixed_release_url"):
                    pynews[lib["library_name"]]["fixed_release_url"] = (
                        bibliotecas[lib["library_name"]]["fixed_release_url"]
                    )
                else:
                    pynews[lib["library_name"]]["releases_urls_list"] = (
                        bibliotecas[lib["library_name"]]["releases_urls_list"]
                    )

    async def main_loop(self, url_name, list_libs):
        tasks = [
            asyncio.ensure_future(self.fetch(self.study_case[lib], url_name))
            for lib in list_libs
        ]
        await asyncio.gather(*tasks)

    async def get(self, url_name):
        await self.main_loop(url_name, list(self.study_case.keys()))


async def main():
    news = PyNews()
    await news.get("releases_url")
    with open(news_json_file, "w", encoding="utf-8") as f:
        dump(pynews, f)
    print(
        f"\033[1;37;44m\033[1;30m\n Edite o arquivo {news_json_file} \
para adicionar as urls contendo o descritivo das novas releases \n"
    )


async def slides():
    print("slides")
    news = PyNews()
    with open(news_json_file, "r", encoding="utf-8") as f:
        news.study_case = json.load(f)
    await news.get("releases_doc_url")
    slides = {}
    try:
        with open("pynews_slides.json", "r", encoding="utf-8") as f:
            slides = json.load(f)
    except Exception:
        pass
    for item in pynews:
        slides[item] = pynews[item]
    with open("pynews_slides.json", "w", encoding="utf-8") as f:
        dump(slides, f)
    print(
        "\033[1;37;44m\033[1;30m\n Abra o arquivo pynews_slides.json para \
ter acesso ao conteúdo produzido.\n"
    )


if __name__ == "__main__":
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("\n \n")
        print(
            "\033[1;37;42m\033[1;30mCommand: python getNews.py releases - \
Gera lista das bibliotecas atualizadas nos últimos \
30 dias\033[0m"
        )
        print("\n")
        print(
            "\033[1;37;44m\033[1;30mCommand: python getNews.py slides - \
Gerar slides a partir da release_url do arquivo \
pynews.json\033[0m"
        )
        print("\n \n")
        sys.exit(0)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if sys.argv[1] == "releases":
        loop.run_until_complete(main())
    elif sys.argv[1] == "slides":
        loop.run_until_complete(slides())
    loop.close()
    sys.exit(0)
