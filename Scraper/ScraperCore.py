import httpx
from ModelData.Result import Result
from logger import get_logger
from bs4 import BeautifulSoup


class ScraperCore:
    def __init__(self):
        self.logger = get_logger("ScraperCore")
        self.headers = {"User-Agent": "RasmusScraper/1.0"}

    async def Scrape(self, webUrls, elements=None):
        async with httpx.AsyncClient(headers=self.headers, timeout=10.0, follow_redirects=True) as client:
            for url in webUrls:
                try:
                    self.logger.info(f"Scraping: {url}")

                    response = await client.get(url)
                    response.raise_for_status()
                    self.logger.success(f"HTTP {response.status_code} OK: {url}")

                    soup = BeautifulSoup(response.text, "html.parser")

                    content_dict: dict[int, str] = {}
                    index = 1

                    if elements is None:
                        for text in soup.stripped_strings:
                            content_dict[index] = text
                            index += 1
                    else:
                        for tag_name in elements:
                            for tag in soup.find_all(tag_name):
                                text = tag.get_text(strip=True)
                                if text:
                                    content_dict[index] = text
                                    index += 1

                    yield Result(url=url, status=response.status_code, content=content_dict)

                except httpx.HTTPError as e:
                    self.logger.error(f"HTTP error for {url}: {e}")
                    yield Result(url=url, status=0, content={1: str(e)})
