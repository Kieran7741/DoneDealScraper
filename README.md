# Done Deal Car Scraper

This repo contains a Beautiful Soup Scraper which scrapes car details from Done deal

## Note
This project was created for learning purposes

## Sample output:
```json
[
    {
      "title": "Ford Fiesta Style 1.25 60 PS  5DR",
      "price": "\u20ac4,950",
      "year": "2011",
      "engine_size": "1.2 Petrol",
      "millage": "134,000 mi",
      "ad_age": "4 days",
      "location": "Kildare",
      "link": "https://www.donedeal.ie/cars-for-sale/ford-fiesta-style-1-25-60-ps-5dr/27603916?campaign=3"
    }
]
```

## Install
Note: This project has only been tested with `python3.9`
1. Clone this repo: `git clone https://github.com/Kieran7741/DoneDealScraper.git && cd DoneDealScraper`
2. Set up enviornment `python3 -m venv .env` 
3. Activate env `source .env/bin/activate`
4. Pip install requirements `pip install -r requirements.txt`

```commandline
# Quick start
git clone https://github.com/Kieran7741/DoneDealScraper.git && cd DoneDealScraper
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Scrape some data
The below example scrapes `5` pages of data for `Ford Fiestas` and saves the data to `cars.json`  
See [done_deal_scraper](./done_deal_scraper.py) for specific implementation
```commandline
python done_deal_scraper.py
```
```python
if __name__ == "__main__":
    # Scrape Ford fiesta details
    fname = "cars.json"
    url = "https://www.donedeal.ie/cars/Ford/Fiesta"

    cars = scrape_number_of_pages(url, 5)
    # cars = scrape_all_pages(url)

    print("Total cars found: ", len(cars))

    # Write to file
    with open(fname, 'w', encoding="utf-8") as outfile:
        print("Writing cars to file:", fname)
        json.dump(cars, outfile)
```

## View the data with Jupyter Lab
Lauch `jupyter-lab` with:
```commandline
jupyter-lab
```
Some sample notebooks can be found in the `notebooks` directory