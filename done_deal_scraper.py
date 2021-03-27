import json
import requests
from bs4 import BeautifulSoup
import time


def extract_car_details(car):
    """
    Extract car details from a car card. Returns a dict with Car details
    :param car: Car card
    :return: {"title": "Ford focus 2018", "price": "\u20ac14,950", "year": "2018", "engine_size": "1.1 Petrol",
     "millage": "19,562 mi", "ad_age": "3 days", "location": "Cork", "link": "https://donedeal.ie/some_car"}
    """
    title_selector = {'class': 'card__body-title'}
    link_selector = {'class': 'card__link'}
    key_info_selector = {'class': 'card__body-keyinfo'}

    year_index = 0
    engine_index = 1
    millage_index = 2
    ad_age_index = 3
    location_index = 4

    car_title = car.find('p', attrs=title_selector).text
    car_link = car.find('a', attrs=link_selector).attrs['href']

    car_details = car.find('ul', attrs=key_info_selector).contents
    if not len(car_details) == 5:
        return
    year = car_details[year_index].text
    engine_size = car_details[engine_index].text
    millage = car_details[millage_index].text
    ad_age = car_details[ad_age_index].text
    location = car_details[location_index].text

    car_price = car.find('div', attrs={'class': 'card__price--left-options'}).find('p', attrs={'class': 'card__price'}).text

    return {"title": car_title, 'price': car_price, 'year': year, "engine_size": engine_size,
            "millage": millage, "ad_age": ad_age, "location": location, "link": car_link}


def scrape_page(base_url="https://www.donedeal.ie/cars", page_number=0, query_params=''):
    """
    Scrape the provided url and page number
    :param base_url: Url to scrape
    :param page_number: Page number to scrape
    :param query_params: Filters to apply
    :return: List of scraped cars
    """
    # Done deal pages contain 28 cars per page
    start = 28 * (page_number-1)

    url = f"{base_url}?start={start}&{query_params}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("div", attrs={'id': "searchResultsPanel"})
    cars = results.contents[0].contents
    car_details = []
    for car in cars:
        try:
            car_detail = extract_car_details(car)
            if car_detail:
                car_details.append(car_detail)
        except Exception as e:
            print(f'Issue parsing car', e)
            pass

    return car_details


def scrape_all_pages(base_url, query_params='', max_pages=20):
    """
    Loop over all pages. Limited to 20 by default to prevent excessive load on server
    :param base_url: Url to scrape
    :param query_params: Filter results
    :param max_pages: Max pages. Override with caution!
    :return:
    """
    cars = []
    page = 1
    while True:
        # Prevent excessive scaping
        if page > max_pages:
            break
        print("Extacting cars from page: ", page)
        try:
            cars.extend(scrape_page(base_url=base_url, page_number=page, query_params=query_params))
            # Trottle requests
            time.sleep(2)
        except:
            print("Could not get details from page number: ", page)
            break
    return cars


def scrape_number_of_pages(base_url, num_pages=10, query_params=''):
    """
    Scrape the provided number of pages
    :param base_url: Url to scrape
    :param num_pages: How many pages to scrape. Try to keep this under 20 to avoid excessive load on Done deal!
    :param query_params: Filter search with query params
    :return: List of car details
    """

    cars = []
    for page in range(1, num_pages + 1):
        print("Extacting cars from page: ", page)
        try:
            cars.extend(scrape_page(base_url=base_url, page_number=page, query_params=query_params))
        except Exception as e:
            # Error likely due to no more results
            print("Error occured", e)
            return
    return cars


if __name__ == "__main__":
    # Scrape Ford fiesta details
    fname = "cars.json"
    url = "https://www.donedeal.ie/cars/Ford/Fiesta"

    cars = scrape_number_of_pages(url, 1)
    # cars = scrape_all_pages(url)

    print("Total cars found: ", len(cars))

    # Write to file
    with open(fname, 'w', encoding="utf-8") as outfile:
        print("Writing cars to file:", fname)
        json.dump(cars, outfile)
