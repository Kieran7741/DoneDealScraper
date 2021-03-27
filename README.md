# Done Deal Car Scraper

This repo contains a Beautiful Soup Scraper which scrapes car details from Done deal

## Sample output:
```json
[{"price": "\u20ac9,950", "year": "2014", "engine_size": "1.2 Petrol", "millage": "44,739 mi", "ad_age": "3 days", "location": "Dublin"},
 {"price": "\u20ac4,950", "year": "2012", "engine_size": "1.4 Diesel", "millage": "159,100 km", "ad_age": "20 hours", "location": "Dublin"}]
```

## Install
Note: This project has only been tested with `python3.9`
1. Clone this repo: `git clone https://github.com/Kieran7741/DoneDealScraper.git && cd DoneDealScraper`
2. Set up enviornment `python3 -m venv .env` 
3. Activate env `source .env/bin/activate`
4. Pip install requirements `pip install -r requirements.txt`

```shell script
# Quick start
git clone https://github.com/Kieran7741/DoneDealScraper.git && cd DoneDealScraper
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Scrape some data
The below example scrapes `5` pages of data for `Ford Fiestas` and saves the data to `cars.json`  
See [done_deal_scraper](./done_deal_scraper.py) for specific implementation
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

