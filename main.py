from Scraper.ScraperCore import ScraperCore
from StorageHandler import StorageHandler

core = ScraperCore()
storage = StorageHandler()

urls = [
    "https://www.dr.dk/presse/dr-k-hele-danmarks-nye-kulturkanal-0",
    "https://nyheder.tv2.dk/samfund/2026-01-27-hun-deler-et-opraab-fra-hospitalet-efter-tab-og-overlaege-bakker-hende-op",
]

for result in core.Scrape(urls):
    storage.save_result(result)
