import asyncio
import json
from Scraper.ScraperCore import ScraperCore
from StorageHandler import StorageHandler

async def main():
    # Load configuration from JSON
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    urls = config.get("domains", [])
    elements = config.get("wanted-elements", None)

    core = ScraperCore()
    storage = StorageHandler()

    async for result in core.CrawlAndScrape(urls, elements=elements):
        storage.save_result(result)

if __name__ == "__main__":
    asyncio.run(main())