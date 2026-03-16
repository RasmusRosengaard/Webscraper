import httpx
from ModelData.Result import Result
from logger import get_logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class ScraperCore:
    def __init__(self):
        self.logger = get_logger("ScraperCore")
        self.headers = {"User-Agent": "RasmusScraper/1.0"}

    def extract_links(self, soup, base_url):
        links = set()
        base_domain = urlparse(base_url).netloc

        for a in soup.find_all("a", href=True):
            href = a["href"]
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)

            if parsed.netloc == base_domain:
                links.add(absolute_url)

        return links

    async def CrawlAndScrape(self, start_urls, elements=None):
        visited = set()
        queue = deque(start_urls)

        async with httpx.AsyncClient(headers=self.headers, timeout=10.0, follow_redirects=True) as client:

            while queue:
                url = queue.popleft()

                if url in visited:
                    continue

                visited.add(url)

                try:
                    self.logger.info(f"Crawling: {url}")

                    response = await client.get(url)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, "html.parser")

                    # ---- your existing scraping logic ----
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

                    # ---- find new links on same domain ----
                    links = self.extract_links(soup, url)

                    for link in links:
                        if link not in visited:
                            queue.append(link)

                    yield Result(url=url, status=response.status_code, content=content_dict)

                except httpx.HTTPError as e:
                    self.logger.error(f"HTTP error for {url}: {e}")
                    yield Result(url=url, status=0, content={1: str(e)})

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