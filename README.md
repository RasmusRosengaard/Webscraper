Features:
Crawling and scraping based on domains and desired elements - choosen from the config file.
Logging system (not persistent)
StorageHandler, output location is choosen in the docker-compose file.
Checking for already scraped urls.

Using yield when scraping, improves memory usuable as it only holds the current result in memory.
