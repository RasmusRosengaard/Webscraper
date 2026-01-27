#### Webscraper

### Guide
To host api: 
uvicorn API.api:app --reload
POST: /scrape
# Example_API: 
Url: http://127.0.0.1:8000/scrape
Body: 
{
  "urls": [
    "https://www.dr.dk/presse/dr-k-hele-danmarks-nye-kulturkanal-0",
    "https://www.dr.dk/nyheder",
    "https://www.dr.dk/nyheder/seneste",
    "https://www.dr.dk/nyheder/regionale/fyn"
  ],
  "elements": ["h1", "p"]
}


# Run locally
Setup urls and elements to scrape in main.py
python .\main.py

### Implemented:
Scrape multiple webpages
Choose specific and multiple html-elements
Terminal logging
Storage
API


### Future work:
Keyword/Sentence Scrape
Subscribe (repeat)
Command Line args
Script to remove duplicate sentences


