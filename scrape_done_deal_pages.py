import json
import requests
from bs4 import BeautifulSoup


def extract_car_details(car):
    key_info_selector = {'class': 'card__body-keyinfo'}
    year_index = 0
    engine_index = 1
    millage_index = 2
    ad_age_index = 3
    location_index = 4

    car_details = car.find('ul', attrs=key_info_selector).contents
    if not len(car_details) == 5:
        return
    year = car_details[year_index].text
    engine_size = car_details[engine_index].text
    millage = car_details[millage_index].text
    ad_age = car_details[ad_age_index].text
    location = car_details[location_index].text

    car_price = car.find('div', attrs={'class': 'card__price--left-options'}).find('p', attrs={'class': 'card__price'}).text

    return {'price': car_price, 'year': year, "engine_size": engine_size,
            "millage": millage, "ad_age": ad_age, "location": location}


def get_done_deal_page(base_url="https://www.donedeal.ie/cars/Ford", page_number=0, query_params=''):

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
            # print(f'Issue parsing car', e)
            pass

    return car_details


def get_all_pages(base_url, query_params=''):
    cars = []
    page = 1
    while True:
        print("Extacting cars from page: ", page)
        try:
            cars.extend(get_done_deal_page(base_url=base_url, page_number=page, query_params=query_params))
        except:
            print("Could not get details from page number: ", page)
            break
    return cars


def get_number_of_pages(base_url, num_pages=10):
    cars = []
    for page in range(1, num_pages):
        print("Extacting cars from page: ", page)
        try:
            cars.extend(get_done_deal_page(base_url=base_url, page_number=page, query_params='mileage_to=50000&transmission=Manual&price_to=15000'))
        except:
            return
    return cars


if __name__ == "__main__":
    fname = "cars.json"
    url = "https://www.donedeal.ie/cars/Ford/Fiesta"
    cars = get_number_of_pages(url, 2)
    # cars = get_all_pages(url)

    print("Total cars found: ", len(cars))

    # Write to file
    with open(fname, 'w', encoding="utf-8") as outfile:
        print("Writing cars to file:", fname)
        json.dump(cars, outfile)
