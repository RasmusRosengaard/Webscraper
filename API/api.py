from fastapi import FastAPI
from typing import List

from logger import get_logger
from Scraper.ScraperCore import ScraperCore
from API.api_models import ScrapeRequest, ScrapeResult


app = FastAPI(
    title="Rasmus Webscraper API",
    version="0.1.0",
)

logger = get_logger("API")
scraper = ScraperCore()


@app.post("/scrape", response_model=List[ScrapeResult])
async def scrape_endpoint(body: ScrapeRequest):
    logger.info(f"Incoming /scrape request: {len(body.urls)} urls")

    results_out: List[ScrapeResult] = []

   
    async for result in scraper.Scrape(body.urls, elements=body.elements):
        results_out.append(
            ScrapeResult(
                url=result.url,
                status=result.status,
                content=result.content,
            )
        )

    logger.success(f"Finished /scrape for {len(body.urls)} urls")
    return results_out
